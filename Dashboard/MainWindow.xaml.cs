using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data;
using System.IO;
using System.IO.Pipes;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;

namespace Dashboard
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        NamedPipeClientStream pipeClient;

        public MainWindow()
        {
            InitializeComponent();
        
            //Asynchronisly runs function
            Task.Run(InitializeNamedPipe);
        }

        /// <summary>
        /// Creates a named pipe and waits for connection, listens for incoming data and sends data
        /// </summary>
        private void InitializeNamedPipe()
        {
            //Create a new named pipe object
            pipeClient = new NamedPipeClientStream(".", "Dashboard_Pipe", PipeDirection.InOut, PipeOptions.Asynchronous);

            Console.WriteLine("Named Pipe established, waiting for connection...");
            //Blocks until connection is established
            pipeClient.Connect();
            Console.WriteLine("Connection Established.");

            Task.Run(() =>
            {
                //Reads data from named pipe
                StreamReader streamReader = new StreamReader(pipeClient);

                while (true)
                {
                    try
                    {
                        // Display the read text to the console
                        string msg;
                        while ((msg = streamReader.ReadLine()) != null)
                        {
                            UpdateConsole("Received from server: " + msg);
                        }
                    }
                    catch (IOException e)
                    {
                        UpdateConsole("ERROR: "  + e.Message);
                    }
                }
            });
        }

        /// <summary>
        /// Called when user presses a key in the input box
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void InputTxt_KeyPressed(object sender, System.Windows.Input.KeyEventArgs e)
        {
            if(e.Key == System.Windows.Input.Key.Enter)
            {
                String msg = InputTxt.Text;
                UpdateConsole("Sending: " + msg);

                //Encode message to be sent to python application
                byte[] encodedMsg = Encoding.ASCII.GetBytes(msg);

                //Write data to named pipe
                pipeClient.Write(encodedMsg, 0, encodedMsg.Length);

                //Reset input text
                InputTxt.Text = "";
                UpdateConsole("Enter message to send: ");
            }
        }

        //Allows ConsoleTxt to be updated from different threads
        private void UpdateConsole(string msg)
        {
            Application.Current.Dispatcher.Invoke(new Action(() => { ConsoleTxt.Text += msg + "\n"; }));
        }
    }
}
