using System;
using System.Runtime.InteropServices;
using System.Timers;
using System.Windows;

namespace ActivityApp
{
    // Esta aplicación tiene un temporizador que se ejecuta cada CheckIdleIntervalInMinutes minutos
    // para analizar el tiempo inactivo del usuario, si es mayor a MaxIdleTimeInMinutes se
    // muestra la ventana de inactividad.
    public partial class App : Application
    {
        private readonly uint CheckIdleIntervalInMinutes = 5;
        private readonly uint MaxIdleTimeInMinutes = 10;
        private static Timer? IdleTimer;
        MainWindow? NW;

        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);

            NW = new();
            NW.Show();

            IdleTimer = new Timer { Interval = CheckIdleIntervalInMinutes * 60 * 1000 };
            IdleTimer.Elapsed += new ElapsedEventHandler(IdleTimerTask);
            IdleTimer.Start();
        }

        private void IdleTimerTask(object? source, ElapsedEventArgs e)
        {
            Current.Dispatcher.Invoke(new Action(() =>
            {
                bool IdleTimeExceeded = IdleTimeFinder.GetIdleTime() > MaxIdleTimeInMinutes * 60 * 1000;
                if (IdleTimeExceeded && (NW == null || !NW.IsActive))
                {
                    NW = new();
                    NW.Show();
                }
            }));
        }

    }

    public class IdleTimeFinder
    {
        [DllImport("User32.dll")]
        private static extern bool GetLastInputInfo(ref LASTINPUTINFO plii);

        [DllImport("Kernel32.dll")]
        private static extern uint GetLastError();

        public static uint GetIdleTime()
        {
            LASTINPUTINFO lastInPut = new LASTINPUTINFO();
            lastInPut.cbSize = (uint)Marshal.SizeOf(lastInPut);
            GetLastInputInfo(ref lastInPut);

            return (uint)Environment.TickCount - lastInPut.dwTime;
        }

        /// Get the Last input time in milliseconds
        public static long GetLastInputTime()
        {
            LASTINPUTINFO lastInPut = new();
            lastInPut.cbSize = (uint)Marshal.SizeOf(lastInPut);
            if (!GetLastInputInfo(ref lastInPut))
            {
                throw new Exception(GetLastError().ToString());
            }
            return lastInPut.dwTime;
        }
    }

    internal struct LASTINPUTINFO
    {
        public uint cbSize;

        public uint dwTime;
    }
}
