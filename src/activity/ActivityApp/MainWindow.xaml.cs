using System;
using System.Timers;
using System.Windows;

namespace ActivityApp
{
    public partial class MainWindow : Window
    {
        private static Timer? shutdownTimer;
        public MainWindow()
        {
            InitializeComponent();
            Topmost = true;

            shutdownTimer = new Timer { Interval = 60000 };
            shutdownTimer.Elapsed += new ElapsedEventHandler(ShutdownTask);
            shutdownTimer.Start();
        }

        private void Btn_Shutdown_Click(object sender, RoutedEventArgs e)
        {
            ShutdownPC();
        }

        private void Btn_Cancel_Click(object sender, RoutedEventArgs e)
        {
            Close();
        }

        private void ShutdownPC()
        {
            // Process.Start("shutdown", "/s /t 0");
            MessageBox.Show("APAGANDO");
            Close();
        }

        private void ShutdownTask(object? source, ElapsedEventArgs e)
        {
            Application.Current.Dispatcher.Invoke(new Action(() =>
            {
                shutdownTimer?.Stop();
                ShutdownPC();
                shutdownTimer?.Start();
            }));            
        }
    }
}
