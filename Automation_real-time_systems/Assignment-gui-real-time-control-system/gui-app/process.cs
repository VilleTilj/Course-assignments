using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Tuni.MppOpcUaClientLib;
using System.Windows.Media;

namespace gui_app
{
    /// <summary>
    /// API to connect to the simulator and handling the events.
    /// </summary>
    public class ConnectOpcUa: IDisposable
    {
        MainWindow gui = null;
        /// <summary>
        /// Create process logic object
        /// </summary>
        public Logic process_logic = null;
        private MppClient client = null;
        private object lock_object = new object();

        // Add public controll variables here
        public double TI300_value = 0;
        public bool E100_val = false;
        public int PI300_val = 0;
        public double TI300_val = 0;
        public bool LS_300_plus = false;
        public bool LS_300_minus = false;
        public int LI400_val = 0;
        public int LI200_val = 0;
        public int LI100_val = 0;
        public bool LA100_val = true;
        public bool P100_P200_PRESET_val = false;
        

        /// <summary>
        /// Process connect class constructor
        /// </summary>
        /// <param name="ui">Mainwindow user interface</param>
        public ConnectOpcUa(MainWindow ui)
        {
            gui = ui;
        }

        /// <summary>
        /// Connects the application to the simulator and its intsruments.
        /// </summary>
        /// <param name="sim_url">Url address to the simulator API</param>
        public void connect(string sim_url)
        {
            try
            {
                // Create connection to the mpp client
                ConnectionParamsHolder conn_params = new ConnectionParamsHolder(sim_url);
                client = new MppClient(conn_params);
                client.ProcessItemsChanged += m_mppClient_ProcessItemsChangedEventHandler;
                client.Init();

                process_logic = new Logic(gui, client, this, lock_object);

                // Add all instruments to the subscription
                add_subscriptions();

                gui.connection_online();
                gui.start.IsEnabled = true;
                gui.connect_button.IsEnabled = false;
            }
            catch (Exception error)
            {
                Console.WriteLine(error);
                gui.connection_offline();
            }
        }

        private void add_subscriptions()
        {
            client.AddToSubscription("E100");
            client.AddToSubscription("FI100");
            client.AddToSubscription("LA+100");
            client.AddToSubscription("LI200");
            client.AddToSubscription("LI100");
            client.AddToSubscription("LI400");
            client.AddToSubscription("LS-200");
            client.AddToSubscription("LS+300");
            client.AddToSubscription("LS-300");
            client.AddToSubscription("P100");
            client.AddToSubscription("P200");
            client.AddToSubscription("P100_P200_PRESET");
            client.AddToSubscription("PI300");
            // Temperature sensors
            client.AddToSubscription("TI100");
            client.AddToSubscription("TI300");
            // Control valve
            client.AddToSubscription("V102");
            client.AddToSubscription("V104");
            // Shut-off Valves
            client.AddToSubscription("V101");
            client.AddToSubscription("V103");
            client.AddToSubscription("V201");
            client.AddToSubscription("V202");
            client.AddToSubscription("V203");
            client.AddToSubscription("V204");
            client.AddToSubscription("V301");
            client.AddToSubscription("V302");
            client.AddToSubscription("V303");
            client.AddToSubscription("V304");
            client.AddToSubscription("V401");
            client.AddToSubscription("V402");
            client.AddToSubscription("V403");
            client.AddToSubscription("V404");
        }


        private void m_mppClient_ProcessItemsChangedEventHandler(object source, ProcessItemChangedEventArgs args)
        {
            foreach(var key in args.ChangedItems.Keys){
                
                switch (key)
                {
                    case "E100":
                        var E100_value = (MppValueBool)args.ChangedItems[key];
                        gui.invoke_E100_value(E100_value.Value);
                        break;

                    case "FI100": break;

                    case "LA+100":
                        var LA100_value = (MppValueBool)args.ChangedItems[key];
                        lock (lock_object)
                        {
                            LA100_val = LA100_value.Value;
                            if (!LA100_val)
                            {
                                gui.trigger_warning();
                            }
                        }
                        break;

                    case "LI100":
                        var LI100_value = (MppValueInt)args.ChangedItems[key];
                        lock (lock_object)
                        {
                            LI100_val = LI100_value.Value;
                            gui.invoke_progress_bars("LI100", LI100_val);
                        }
                        break;

                    case "LI200":
                        var LI200_value = (MppValueInt)args.ChangedItems[key];
                        lock (lock_object)
                        {
                            LI200_val = LI200_value.Value;
                            gui.invoke_progress_bars("LI200", LI200_val);
                        }
                        break;


                    case "LI400":
                        var LI400_value = (MppValueInt)args.ChangedItems[key];
                        lock (lock_object)
                        {
                            LI400_val = LI400_value.Value;
                            gui.invoke_progress_bars("LI400", LI400_val);
                        }
                        break;

                    case "LS-200":
                    case "LS+300":
                        var LS300_plus_value = (MppValueBool)args.ChangedItems[key];
                        lock (lock_object)
                        {
                            LS_300_plus = LS300_plus_value.Value;
                            gui.invoke_LI300_plus_status(LS_300_plus);
                    
                        }
                        break;
                    case "LS-300":
                        var LS300_minus_value = (MppValueBool)args.ChangedItems[key];
                        lock (lock_object)
                        {
                            LS_300_minus = LS300_minus_value.Value;
                            gui.invoke_LS300_minus_status(LS_300_minus);
                        }
                        break;
                    case "P100":
                        var P100_value = (MppValueInt)args.ChangedItems[key];
                        var P100 = P100_value.Value;
                        gui.invoke_pumps("P100", P100.ToString());
                        break;

                    case "P200":
                        var P200_value = (MppValueInt)args.ChangedItems[key];
                        var P200 = P200_value.Value;
                        gui.invoke_pumps("P200", P200.ToString());
                        break;

                    case "P100_P200_PRESET":
                        var pump_preset = (MppValueBool)args.ChangedItems[key];
                        var preset = pump_preset.Value;
                        P100_P200_PRESET_val = preset;
                        break;

                    case "PI300":
                        var PI300_value = (MppValueInt)args.ChangedItems[key];
                        var PI300 = PI300_value.Value;
                        lock (lock_object)
                        {
                            PI300_val = PI300;
                            gui.invoke_PI300_value(PI300_val.ToString());
                        }
                        break;
                    
                    case "TI100":
                        var TI100_value = (MppValueDouble)args.ChangedItems[key];
                        var TI100 = Math.Round(TI100_value.Value, 2);
                        gui.change_TI100_value(TI100.ToString());
                        break;

                    case "TI300":
                        var TI300 = (MppValueDouble)args.ChangedItems[key];
                        TI300_value = Math.Round(TI300.Value, 2);
                        lock (lock_object)
                        {
                            TI300_val = TI300_value;
                            gui.change_TI300_value(TI300_val.ToString());
                        }
                        break;

                    case "V101":
                        var v101_value = (MppValueBool)args.ChangedItems[key];
                        var v101 = v101_value.Value;
                        gui.invoke_valve_onoff("v101", v101);
                        break;
                        
                    case "V102":
                        var v102_value = (MppValueInt)args.ChangedItems[key];
                        var v102 = v102_value.Value;
                        gui.invoke_valve_control("v102", v102.ToString());
                        break;

                    case "V103":
                        var v103_value = (MppValueBool)args.ChangedItems[key];
                        var v103 = v103_value.Value;
                        gui.invoke_valve_onoff("v103", v103);
                        break;

                    case "V104":
                        var v104_value = (MppValueInt)args.ChangedItems[key];
                        var v104 = v104_value.Value;
                        gui.invoke_valve_control("v104", v104.ToString());
                        break;
                    case "V201":
                        var v201_value = (MppValueBool)args.ChangedItems[key];
                        var v201 = v201_value.Value;
                        gui.invoke_valve_onoff("v201", v201);
                        break;

                    case "V202":
                        var v202_value = (MppValueBool)args.ChangedItems[key];
                        var v202 = v202_value.Value;
                        gui.invoke_valve_onoff("v202", v202);
                        break;

                    case "V203":
                        var v203_value = (MppValueBool)args.ChangedItems[key];
                        var v203 = v203_value.Value;
                        gui.invoke_valve_onoff("v203", v203);
                        break;

                    case "V204":
                        var v204_value = (MppValueBool)args.ChangedItems[key];
                        var v204 = v204_value.Value;
                        gui.invoke_valve_onoff("v204", v204);
                        break;

                    case "V301":
                        var v301_value = (MppValueBool)args.ChangedItems[key];
                        var v301 = v301_value.Value;
                        gui.invoke_valve_onoff("v301", v301);
                        break;
                    case "V302":
                        var v302_value = (MppValueBool)args.ChangedItems[key];
                        var v302 = v302_value.Value;
                        gui.invoke_valve_onoff("v302", v302);
                        break;
                    case "V303":
                        var v303_value = (MppValueBool)args.ChangedItems[key];
                        var v303 = v303_value.Value;
                        gui.invoke_valve_onoff("v303", v303);
                        break;
                    case "V304":
                        var v304_value = (MppValueBool)args.ChangedItems[key];
                        var v304 = v304_value.Value;
                        gui.invoke_valve_onoff("v304", v304);
                        break;
                    case "V401":
                        var v401_value = (MppValueBool)args.ChangedItems[key];
                        var v401 = v401_value.Value;
                        gui.invoke_valve_onoff("v401", v401);
                        break;
                    case "V402":
                        var v402_value = (MppValueBool)args.ChangedItems[key];
                        var v402 = v402_value.Value;
                        gui.invoke_valve_onoff("v402", v402);
                        break;
                    case "V403": 
                        var v403_value = (MppValueBool)args.ChangedItems[key];
                        var v403 = v403_value.Value;
                        gui.invoke_valve_onoff("v403", v403);
                        break;
                    case "V404":
                        var v404_value = (MppValueBool)args.ChangedItems[key];
                        var v404 = v404_value.Value;
                        gui.invoke_valve_onoff("v404", v404);
                        break;
                }
                
            }
                
        }

        /// <summary>
        /// Dispose the opc ua client connection and set the gui to show connection offline.
        /// </summary>
        public void Dispose()
        { 
            // Closes the process and the connection
            try
            {
                if (client != null)
                {
                    client.Dispose();
                    client = null;
                    gui.statuslabel.Text = "OFFLINE";
                    gui.statuslabel.Foreground = Brushes.Red;
                }
            }
            catch(Exception e)
            {

            }
        }
    }
}