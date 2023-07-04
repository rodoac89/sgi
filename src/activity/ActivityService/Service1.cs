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
    using Microsoft.Win32;

    public partial class Service1 : ServiceBase
    {
        private readonly string SERVICE_NAME = "Activity";
        // private static string DOMAIN = "127.0.0.1:8000";
        private static string DOMAIN = "labs-activity.up.railway.app";
        // private readonly string WORKSTATION = "A1-COM101PC02";
        private readonly string WORKSTATION = Environment.MachineName;
        private string API_BASE_URI = $"https://{DOMAIN}/api/";
        private readonly string START_ENDPOINT = "activity/session/start";
        private readonly string END_ENDPOINT = "activity/session/end";
        private string WEBSOCKET_BASE_URI = $"wss://{DOMAIN}/";
        private readonly string WEBSOCKET_ENDPOINT = "ws/activity/";
        private readonly string WEBSOCKET_SECRET = "gUkXp2s5v8y/B?E(G+KbPeShVmYq3t6w";

        static readonly HttpClient httpClient = new HttpClient();
        private readonly ClientWebSocket webSocket = new ClientWebSocket();
        private Timer aliveTimer;
        private long startTimestamp;

        public Service1()
        {
            startTimestamp = GetCurrentTimestamp();

            InitializeComponent();

            ServiceName = SERVICE_NAME;

            RegistryKey key = Registry.LocalMachine.OpenSubKey("Software\\ActivityService\\Values");
            if (key != null)
            {
                object registeredDomain = key.GetValue("DOMAIN");
                if (registeredDomain != null)
                {
                    DOMAIN = registeredDomain.ToString();
                    API_BASE_URI = $"https://{DOMAIN}/api/";
                    WEBSOCKET_BASE_URI = $"wss://{DOMAIN}/";
                }
                key.Close();
            }

            // Configurar Http Client.
            httpClient.BaseAddress = new Uri(API_BASE_URI);
            httpClient.DefaultRequestHeaders
              .Accept
              .Add(new MediaTypeWithQualityHeaderValue("application/json"));

            aliveTimer = new Timer(10000);
            aliveTimer.Elapsed += SendAliveMessage;
            aliveTimer.Enabled = true;
        }

        protected override void OnStart(string[] args)
        {
            SendStartRequest();
            ConnectWebSocket();
        }

        protected override void OnStop()
        {
        }

        protected override void OnShutdown()
        {
            // Enviar mensaje de finalizar sesión por Websocket si no hacerlo por HTTP
            try
            {
                var keyValueList = new List<(string key, string value)> { ("type", "end") };
                SendWSMessage(keyValueList);
            }
            catch (Exception)
            {
                SendEndRequest();
            }

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

        private void SendEndRequest()
        {
            string uri = $"{API_BASE_URI}{END_ENDPOINT}";

            var values = new Dictionary<string, string>
            {
                { "ws", WORKSTATION },
                { "start", startTimestamp.ToString() },
                { "timestamp", GetCurrentTimestamp().ToString() }
            };

            var content = new FormUrlEncodedContent(values);

            httpClient.PostAsync(uri, content);
        }

        private async void ConnectWebSocket()
        {
            string eKey = AESEncrypt(WORKSTATION, WEBSOCKET_SECRET);
            EventLog.WriteEntry(eKey, EventLogEntryType.Error);
            string uri = $"{WEBSOCKET_BASE_URI}{WEBSOCKET_ENDPOINT}{eKey}/";
            // string uri = $"{WEBSOCKET_BASE_URI}{WEBSOCKET_ENDPOINT}{WORKSTATION}/";
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

