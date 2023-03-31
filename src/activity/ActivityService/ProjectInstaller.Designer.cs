namespace ActivityService
{
    partial class ProjectInstaller
    {
        /// <summary>
        /// Variable del diseñador necesaria.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary> 
        /// Limpiar los recursos que se estén usando.
        /// </summary>
        /// <param name="disposing">true si los recursos administrados se deben desechar; false en caso contrario.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Código generado por el Diseñador de componentes

        /// <summary>
        /// Método necesario para admitir el Diseñador. No se puede modificar
        /// el contenido de este método con el editor de código.
        /// </summary>
        private void InitializeComponent()
        {
            this.ActivityServiceProcessInstaller = new System.ServiceProcess.ServiceProcessInstaller();
            this.ActivityServiceInstaller = new System.ServiceProcess.ServiceInstaller();
            // 
            // ActivityServiceProcessInstaller
            // 
            this.ActivityServiceProcessInstaller.Account = System.ServiceProcess.ServiceAccount.LocalSystem;
            this.ActivityServiceProcessInstaller.Password = null;
            this.ActivityServiceProcessInstaller.Username = null;
            // 
            // ActivityServiceInstaller
            // 
            this.ActivityServiceInstaller.ServiceName = "ActivityService";
            this.ActivityServiceInstaller.StartType = System.ServiceProcess.ServiceStartMode.Automatic;
            this.ActivityServiceInstaller.AfterInstall += new System.Configuration.Install.InstallEventHandler(this.ActivityServiceInstaller_AfterInstall);
            // 
            // ProjectInstaller
            // 
            this.Installers.AddRange(new System.Configuration.Install.Installer[] {
            this.ActivityServiceProcessInstaller,
            this.ActivityServiceInstaller});

        }

        #endregion

        private System.ServiceProcess.ServiceProcessInstaller ActivityServiceProcessInstaller;
        private System.ServiceProcess.ServiceInstaller ActivityServiceInstaller;
    }
}