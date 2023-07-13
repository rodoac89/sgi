using System.Diagnostics;
using System.Timers;
using System.Windows;

namespace ActivityApp
{
    public partial class MainWindow : Window
    {
        private readonly uint ShutdownTimerIntervalInSeconds = 60;
        private static Timer? ShutdownTimer;
        public MainWindow()
        {
            InitializeComponent();
            Topmost = true;

            // Cuando se acaba el tiempo se apaga el PC, a menos que se presione el botón
            // cancelar.
            ShutdownTimer = new Timer { Interval = ShutdownTimerIntervalInSeconds * 1000 };
            ShutdownTimer.Elapsed += new ElapsedEventHandler(ShutdownTask);
            ShutdownTimer.Start();
        }

        private void Btn_Shutdown_Click(object sender, RoutedEventArgs e)
        {
            ShutdownPC();
        }

        private void Btn_Cancel_Click(object sender, RoutedEventArgs e)
        {
            ShutdownTimer?.Stop();
            Close();
        }

        private void ShutdownPC()
        {
            ShutdownTimer?.Stop();
            Process.Start("shutdown", "/s /t 0");
            Close();
        }

        private void ShutdownTask(object? source, ElapsedEventArgs e)
        {
            ShutdownPC();
        }
    }
}
