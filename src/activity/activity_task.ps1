Add-Type @'
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

namespace PInvoke.Win32 {

    public static class UserInput {

        [DllImport("user32.dll", SetLastError=false)]
        private static extern bool GetLastInputInfo(ref LASTINPUTINFO plii);

        [StructLayout(LayoutKind.Sequential)]
        private struct LASTINPUTINFO {
            public uint cbSize;
            public int dwTime;
        }

        public static DateTime LastInput {
            get {
                DateTime bootTime = DateTime.UtcNow.AddMilliseconds(-Environment.TickCount);
                DateTime lastInput = bootTime.AddMilliseconds(LastInputTicks);
                return lastInput;
            }
        }

        public static double IdleTime {
            get {
                return DateTime.UtcNow.Subtract(LastInput).TotalMilliseconds;
            }
        }

        public static int LastInputTicks {
            get {
                LASTINPUTINFO lii = new LASTINPUTINFO();
                lii.cbSize = (uint)Marshal.SizeOf(typeof(LASTINPUTINFO));
                GetLastInputInfo(ref lii);
                return lii.dwTime;
            }
        }
    }
}
'@

while ( $true ) {
    Start-Sleep -Milliseconds 5000 # 5 minutes
    $idleTime = [PInvoke.Win32.UserInput]::IdleTime
    if ( $idleTime -gt 10000 ) {
        Start-Process -FilePath "C:\Users\fperez\Documentos\proyectos\ActivityApp\bin\Debug\net6.0-windows\ActivityApp.exe"
    }
}