using System.ServiceProcess;

namespace ActivityService
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Net.Http;
    using System.Net.Http.Headers;
    using System.Runtime.InteropServices;    
    using System.Text;
    using System.Threading.Tasks;
    using System.Timers;


    public partial class Service1 : ServiceBase
    {
        private readonly string SERVICE_NAME = "ActivityService";
        private readonly string LOG_SOURCE = "ActivityLogSource";
        private readonly string lOGGER_NAME = "ActivityLog";
        // private readonly string workstation = Environment.MachineName;
        private readonly string WORKSTATION = "A1-COM103PC01";
        //private readonly string apiBaseUri = "http://127.0.0.1:8000/api/";
        private readonly string API_BASE_URI = "https://express-example-api-production.up.railway.app/api/";
        private readonly string SESSION_ENDPOINT = "activity/session";        
        private readonly string POPUP_TITLE = "Alerta Inactividad";
        private readonly string POPUP_MSG = "El equipo se apagará por inactividad en menos de un minuto, para prevenir cierra esta ventana o presiona Cancelar";
        private readonly int ALIVE_INTERVAL = 60000;
        private readonly int SHUTDOWN_INTERVAL = 15 * 60000;
        private readonly int IDLE_TIME_TO_SHUTDOWN = 10000;

        public static IntPtr WTS_CURRENT_SERVER_HANDLE = IntPtr.Zero;

        static readonly HttpClient httpClient = new HttpClient();
        private readonly EventLog eventLog;
        private Timer shutdownTimer;
        private long startTimestamp;
        private long endTimestamp;
        private int aliveSignals = 0;

        public Service1()
        {
            InitializeComponent();

            ServiceName = SERVICE_NAME;

            // Configurar Logs.
            eventLog = EventLog;
            if (!EventLog.SourceExists(LOG_SOURCE))
            {
                EventLog.CreateEventSource(
                    LOG_SOURCE, lOGGER_NAME);
            }
            eventLog.Source = LOG_SOURCE;
            eventLog.Log = lOGGER_NAME;

            // Configurar Http Client.
            httpClient.BaseAddress = new Uri(API_BASE_URI);
            httpClient.DefaultRequestHeaders
              .Accept
              .Add(new MediaTypeWithQualityHeaderValue("application/json"));
        }

        protected override void OnStart(string[] args)
        {
            // Enviar señal de startup al servidor.
            PostSessionStart();

            // Configurar un timer que envie señal de vida cada 1 minuto.
            Timer aliveTimer = new Timer { Interval = ALIVE_INTERVAL };
            aliveTimer.Elapsed += new ElapsedEventHandler(PostAliveTask);
            aliveTimer.Start();

            // Configurar un timer que obtenga el tiempo de inactividad (sin input) de usuario para apagar el computador.
            shutdownTimer = new Timer { Interval = SHUTDOWN_INTERVAL };
            shutdownTimer.Elapsed += new ElapsedEventHandler(ShutdownTask);
            shutdownTimer.Start();
        }

        protected override void OnStop()
        {
            eventLog.WriteEntry($"Se ha detenido el servicio.", EventLogEntryType.Warning);
        }

        protected override void OnShutdown()
        {
            PostSessionEnd();

            base.OnShutdown();
        }

        private async void PostSessionStart()
        {
            startTimestamp = GetCurrentTimestamp();
            HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Post, $"{SESSION_ENDPOINT}/start");

            List<(string key, string value)> sessionStart = new List<(string key, string value)>
                { ("pc", WORKSTATION), ("timestamp", startTimestamp.ToString()) };

            request.Content = new StringContent(GetJsonString(sessionStart), Encoding.UTF8, "application/json");
            bool canPost = false;
            while (!canPost)
            {
                HttpResponseMessage response = await httpClient.SendAsync(request);
                canPost = response.IsSuccessStatusCode;
                if (!canPost)
                {
                    eventLog.WriteEntry($"No se ha enviado correctamente el inicio de sesión. Reintentando..", EventLogEntryType.Warning);
                    await Task.Delay(3000);
                }

            }
            eventLog.WriteEntry($"Se ha enviado correctamente el inicio de sesión.", EventLogEntryType.Information);
        }

        private async void PostSessionEnd()
        {
            endTimestamp = GetCurrentTimestamp();
            HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Post, $"{SESSION_ENDPOINT}/end");

            List<(string key, string value)> sessionEnd = new List<(string key, string value)>
                { ("pc", WORKSTATION), ("start", startTimestamp.ToString()), ("timestamp", endTimestamp.ToString()) };

            request.Content = new StringContent(GetJsonString(sessionEnd), Encoding.UTF8, "application/json");
            HttpResponseMessage response = await httpClient.SendAsync(request);
            if (response.IsSuccessStatusCode)
            {
                eventLog.WriteEntry($"Se ha enviado correctamente la señal de apagado al servidor.", EventLogEntryType.Information);
            }
            else
            {
                eventLog.WriteEntry($"Ha ocrrido un problema al enviar la señal de apagado al servidor. \n{response.Content}", EventLogEntryType.Error);
            }            
        }

        private async void PostAliveTask(object sender, ElapsedEventArgs args)
        {
            aliveSignals++;
            HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Post, $"{SESSION_ENDPOINT}/alive");

            List<(string key, string value)> sessionAlive = new List<(string key, string value)>
                { ("pc", WORKSTATION), ("start", startTimestamp.ToString()), ("timestamp", GetCurrentTimestamp().ToString()) };

            request.Content = new StringContent(GetJsonString(sessionAlive), Encoding.UTF8, "application/json");
            HttpResponseMessage response = await httpClient.SendAsync(request);
            if (!response.IsSuccessStatusCode)
            {
                eventLog.WriteEntry($"No se ha enviado correctamente la señal de vida {aliveSignals}", EventLogEntryType.Warning);
            }
            else if (aliveSignals % 30 == 0)
            {
                eventLog.WriteEntry($"Se ha enviado la señal de vida número {aliveSignals}", EventLogEntryType.Information);
            }
        }

        private void ShutdownTask(object sender, ElapsedEventArgs args)
        {
            uint idleTime = GetIdleTime();
            if (idleTime > IDLE_TIME_TO_SHUTDOWN)
            {
                int response = GetIdleMessageResponse();
                if (response == -1)
                {
                    eventLog.WriteEntry("No se ha encontrado el usuario activo para enviar mensaje de inactividad.", EventLogEntryType.Error);
                }
                else if (response == 32000 || response == 1)
                {
                    eventLog.WriteEntry("El PC se apagará por inactividad", EventLogEntryType.Information);                    
                    Process.Start(new ProcessStartInfo("shutdown", "/s /t 0") { CreateNoWindow = true, UseShellExecute = false });
                    shutdownTimer.Stop();
                }
            }
        }

        private int GetIdleMessageResponse()
        {
            for (int userSession = 10; userSession > 0; userSession--)
            {
                try
                {
                    bool result = WTSSendMessage(
                        WTS_CURRENT_SERVER_HANDLE,
                        userSession,
                        POPUP_TITLE,
                        POPUP_TITLE.Length,
                        POPUP_MSG,
                        POPUP_MSG.Length,
                        1,
                        10,
                        out int response,
                        true);
                    int err = Marshal.GetLastWin32Error();
                    if (err == 0 && result)
                    {
                        return response;
                    }
                }
                catch (Exception ex)
                {
                    eventLog.WriteEntry($"Error enviando mensaje de inactividad.\n{ex.Message}", EventLogEntryType.Error);
                    return -2;                    
                }
            }
            return -1;
        }

        private long GetCurrentTimestamp()
        {
            DateTime dt = DateTime.Now;
            return ((DateTimeOffset)dt).ToUnixTimeMilliseconds();
        }        

        // TODO : quitar esta funcion, porque solo sirve en programas de escritorio.
        private uint GetIdleTime()
        {
            uint idleTime = 0;
            LASTINPUTINFO lastInputInfo = new LASTINPUTINFO();
            lastInputInfo.cbSize = (uint)Marshal.SizeOf(lastInputInfo);
            lastInputInfo.dwTime = 0;

            uint envTicks = (uint)Environment.TickCount;

            if (GetLastInputInfo(ref lastInputInfo))
            {
                uint lastInputTick = lastInputInfo.dwTime;

                idleTime = envTicks - lastInputTick;
            }

            eventLog.WriteEntry($"Idle time: {idleTime}", EventLogEntryType.Error);
            return ((idleTime > 0) ? idleTime : 0);
        }

        private string GetJsonString(List<(string key, string value)> entries)
        {
            string jsonString = "{";
            foreach ((string key, string value) in entries)
            {
                if (Int64.TryParse(value, out long timestamp))
                {
                    jsonString += "\"" + key + "\":" + timestamp + ",";
                }
                else
                {
                    jsonString += "\"" + key + "\":\"" + value + "\",";
                }
            }
            jsonString = jsonString.Remove(jsonString.Length - 1) + "}";
            return jsonString;
        }

        [DllImport("User32.dll")]
        static extern bool GetLastInputInfo(ref LASTINPUTINFO plii);

        [DllImport("wtsapi32.dll", SetLastError = true)]
        static extern bool WTSSendMessage(
            IntPtr hServer,
            [MarshalAs(UnmanagedType.I4)] int SessionId,
            string pTitle,
            [MarshalAs(UnmanagedType.U4)] int TitleLength,
            string pMessage,
            [MarshalAs(UnmanagedType.U4)] int MessageLength,
            [MarshalAs(UnmanagedType.U4)] int Style,
            [MarshalAs(UnmanagedType.U4)] int Timeout,
            [MarshalAs(UnmanagedType.U4)] out int pResponse,
            bool bWait);

        internal struct LASTINPUTINFO
        {
            public uint cbSize;

            public uint dwTime;
        }

    }
}

