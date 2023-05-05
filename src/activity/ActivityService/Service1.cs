using System.ServiceProcess;

namespace ActivityService
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Net.Http;
    using System.Net.Http.Headers;
    using System.Net.WebSockets;  
    using System.Text;
    using System.Security.Cryptography;
    using System.Timers;

    public partial class Service1 : ServiceBase
    {
        private readonly string SERVICE_NAME = "ActivityService";
        private readonly string LOG_SOURCE = "ActivityLogSource";
        private readonly string LOGGER_NAME = "ActivityLog";
        // private readonly string workstation = Environment.MachineName;
        private static readonly string HOST = "127.0.0.1:8000";
        //private static readonly string HOST = "labsadmin.vulpinesoft.net";
        private readonly string WORKSTATION = "A1-COM103PC03";        
        private readonly string API_BASE_URI = $"http://{HOST}/api/";
        private readonly string START_ENDPOINT = "activity/session/start";
        private readonly string WEBSOCKET_BASE_URI = $"ws://{HOST}/";
        private readonly string WEBSOCKET_ENDPOINT = "ws/activity/enc/";
        private readonly string WEBSOCKET_SECRET = "gUkXp2s5v8y/B?E(G+KbPeShVmYq3t6w";

        public static IntPtr WTS_CURRENT_SERVER_HANDLE = IntPtr.Zero;

        
        private readonly EventLog eventLog;
        static readonly HttpClient httpClient = new HttpClient();
        private readonly ClientWebSocket webSocket = new ClientWebSocket();
        private Timer aliveTimer;
        private long startTimestamp;

        public Service1()
        {
            InitializeComponent();

            startTimestamp = GetCurrentTimestamp();

            ServiceName = SERVICE_NAME;

            // Configurar Logs.
            eventLog = EventLog;
            if (!EventLog.SourceExists(LOG_SOURCE))
            {
                EventLog.CreateEventSource(
                    LOG_SOURCE, LOGGER_NAME);
            }
            eventLog.Source = LOG_SOURCE;
            eventLog.Log = LOGGER_NAME;

            // Configurar Http Client.
            httpClient.BaseAddress = new Uri(API_BASE_URI);
            httpClient.DefaultRequestHeaders
              .Accept
              .Add(new MediaTypeWithQualityHeaderValue("application/json"));

            aliveTimer = new Timer(2000);
            aliveTimer.Elapsed += SendAliveMessage;
            aliveTimer.Enabled = true;
        }

        protected override void OnStart(string[] args)
        {
            SendStartRequest();
            // Conectar el web socket.
            ConnectWebSocket();
        }

        protected override void OnStop()
        {
        }

        protected override void OnShutdown()
        {
            base.OnShutdown();
        }

        private void SendStartRequest()
        {
            string uri = $"{API_BASE_URI}{START_ENDPOINT}";

            var values = new Dictionary<string, string>
            {
                { "ws", WORKSTATION },
                { "timestamp", startTimestamp.ToString() }
            };

            var content = new FormUrlEncodedContent(values);

            httpClient.PostAsync(uri, content);
        }

        private async void ConnectWebSocket()
        {
            string eKey = AESEncrypt(WORKSTATION, WEBSOCKET_SECRET);
            EventLog.WriteEntry(eKey, EventLogEntryType.Error);
            string uri = $"{WEBSOCKET_BASE_URI}{WEBSOCKET_ENDPOINT}{eKey}";
            await webSocket.ConnectAsync(new Uri(uri), System.Threading.CancellationToken.None);

            var keyValueList = new List<(string key, string value)> { ("type", "start") };
            SendWSMessage(keyValueList);
        }

        private void SendAliveMessage(Object source, ElapsedEventArgs e)
        {
            var keyValueList = new List<(string key, string value)> { ("type", "alive") };
            SendWSMessage(keyValueList);
        }

        private async void SendWSMessage(List<(string key, string value)> keyValueList)
        {
            string payload = GetJsonString(keyValueList);
            var encoded = Encoding.UTF8.GetBytes(payload);
            var buffer = new ArraySegment<byte>(encoded, 0, encoded.Length);
            await webSocket.SendAsync(buffer, WebSocketMessageType.Text, true, System.Threading.CancellationToken.None);
        }

        private string GetJsonString(List<(string key, string value)> entries)
        {
            string jsonString = "{";
            foreach ((string key, string value) in entries)
            {
                if (long.TryParse(value, out long timestamp))
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

        private long GetCurrentTimestamp()
        {
            DateTime dt = DateTime.Now;
            return ((DateTimeOffset)dt).ToUnixTimeMilliseconds();
        }

        private string AESEncrypt(string plaintext, string key)
        {
            byte[] keyBytes = Encoding.UTF8.GetBytes(key);

            using (Aes aes = Aes.Create())
            {
                aes.KeySize = 256;
                aes.BlockSize = 128;
                aes.Key = keyBytes;
                aes.IV = new byte[16]; // Vector de inicialización

                ICryptoTransform encryptor = aes.CreateEncryptor(aes.Key, aes.IV);

                byte[] plaintextBytes = Encoding.UTF8.GetBytes(plaintext);
                byte[] ciphertextBytes = encryptor.TransformFinalBlock(plaintextBytes, 0, plaintextBytes.Length);

                return Convert.ToBase64String(ciphertextBytes);
            }
        }

    }
}

