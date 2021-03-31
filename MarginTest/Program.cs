using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using Impinj.OctaneSdk;


namespace MarginTest
{
    public class Reader
    {

        //array to hold the margin test settings
        //public double currentPower = 0;

        public void ConnectReader(ImpinjReader reader, string hostname, double startPower)
        {
            try {
                Console.WriteLine("Attempting to connect to reader: " + hostname);
                reader.Connect(hostname);
                //connected = true;

                Console.WriteLine("Loading Margin Test Settings onto the reader");

                Settings settings= reader.QueryDefaultSettings();

                settings.Report.IncludeAntennaPortNumber = true;
                settings.Report.Mode = ReportMode.Individual;
                settings.Antennas.TxPowerInDbm = startPower;
                settings.Report.IncludeFastId = true;
                settings.Session = 0;
                settings.SearchMode = SearchMode.SingleTarget;

                reader.ApplySettings(settings);
                Console.WriteLine("Successfully connected, settings Applied");

            }
            catch (OctaneSdkException err)
            {
                System.Diagnostics.Trace.
                    WriteLine("An Octane Exception has occurred: {0}", err.Message);
            }
            catch (Exception err)
            {
                System.Diagnostics.Trace.
                    WriteLine("An Exception has occured: {0}", err.Message);
            }
        }

        public double UpdateSettings(ImpinjReader reader, double power, double stepSize)
        {
            Settings settings = reader.QuerySettings();
            settings.Antennas.TxPowerInDbm = power + stepSize;
            reader.ApplySettings(settings);
            Console.WriteLine("Power Level successfully changed");

            return power + stepSize;
        }

    }
    class Program 
    {
        public static List<string> tagsRead = new List<string>();
        public static void onTagsReported(ImpinjReader reader, TagReport report)
        {
            //string file = "temp.csv";
            //var settings = reader.QuerySettings();
            foreach (Tag tag in report)
            {
                var tagData = tag.LastSeenTime.ToString() + "," + tag.Epc.ToString() + ",";
                Console.WriteLine(tagData);
                tagsRead.Add(tagData);
            }
        }

        public static void WriteFileName(List<string> tagsRead, string tagName, double currentPower)
        {
            string currentPowerAsString = currentPower.ToString();
            string dataDir = System.AppDomain.CurrentDomain.BaseDirectory.ToString() + "\\data\\" + tagName + "\\";
            Console.WriteLine(dataDir);
            if (!Directory.Exists(dataDir))
            {
                System.IO.Directory.CreateDirectory(dataDir);
            }
            string newFile = dataDir + tagName + currentPowerAsString + ".csv";
            if (!File.Exists(newFile))
            {
                string header ="timestamp" + "," + "epc" + "," + "power" +"\n";
                File.WriteAllText(newFile, header);
                File.AppendAllLines(newFile, tagsRead);
            }
            else
            {
                File.AppendAllLines(newFile, tagsRead);
            }
            
        }

        static void Main(string[] args)
        {
            Reader readerObject = new Reader();
            ImpinjReader reader = new ImpinjReader();
            Stopwatch s = new Stopwatch();
            /*
                ARGUMENTS IN ORDER:
                0: Hostname
                1: Start Power
                2: End Power
                3: Step Size
                4: Power Duration
                5: CSV File name
            */
            // variable initialization
            string hostname = args[0];
            double startPower = Convert.ToDouble(args[1]);
            double endPower = Convert.ToDouble(args[2]);
            double stepSize = Convert.ToDouble(args[3]);
            int duration = Convert.ToInt32(args[4]);
            string tagName = args[5];
            double currentPower = startPower;

            // start the margin test
            readerObject.ConnectReader(reader, hostname, currentPower);
            // creating event for when a tag is reportedi

            reader.TagsReported += onTagsReported;


            while (currentPower <= endPower)
            {
                if (reader.IsConnected)
                {
                    reader.Start();
                    s.Start();
                    while (s.Elapsed < TimeSpan.FromSeconds(duration))
                    {
                        //Console.WriteLine("This is a test");
                    }
                    s.Reset();
                    reader.Stop();
                    WriteFileName(tagsRead, tagName, currentPower);
                    // clearing list contents to make room for the next powerlevel
                    tagsRead.Clear();
                    // updating the power setting before running the test again
                    currentPower = readerObject.UpdateSettings(reader, currentPower, stepSize);
                }
                else
                {
                    Console.Write("Reader not connected! ");
                    System.Environment.Exit(1);
                }
                Console.WriteLine("Finished A power cycle");
                
            }

            Console.WriteLine("Margin test completed. Moving Outputs to /data");
            reader.Disconnect();
            
        }
    }
}