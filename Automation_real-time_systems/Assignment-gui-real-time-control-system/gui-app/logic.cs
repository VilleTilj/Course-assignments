using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Tuni.MppOpcUaClientLib;
using System.Windows.Media;
using System.Threading.Tasks;
using System.Threading;
using System.Diagnostics;

namespace gui_app
{
    /// <summary>
    /// MVC models Control logic. Is responsible for controlling actuators and the process.
    /// </summary>
    public class Logic
    {
        MainWindow _ui = null;
        MppClient _client = null;
        ConnectOpcUa _connection = null;
        Control _control = null;
        object _lock_object = null;
        private int hold_time = 200;

        /// <summary>
        /// Logic class constructor
        /// </summary>
        /// <param name="ui">User interface object</param>
        /// <param name="client">mppc client object</param>
        /// <param name="connection">Connection class obect</param>
        /// <param name="lock_object">Lock object</param>
        public Logic(MainWindow ui, MppClient client, ConnectOpcUa connection, object lock_object)
        {
            _ui = ui;
            _client = client;
            _connection = connection;
            _lock_object = lock_object;
        }


        /// <summary>
        /// Method to shut down all actuators
        /// </summary>
        public void shutdown_process()
        {
            _client.SetOnOffItem("E100", false);
            _client.SetOnOffItem("P100_P200_PRESET", false);
            _client.SetOnOffItem("V103", false);
            _client.SetOnOffItem("V101", false);
            _client.SetOnOffItem("V201", false);
            _client.SetOnOffItem("V202", false);
            _client.SetOnOffItem("V203", false);
            _client.SetOnOffItem("V204", false);
            _client.SetOnOffItem("V301", false);
            _client.SetOnOffItem("V302", false);
            _client.SetOnOffItem("V303", false);
            _client.SetOnOffItem("V304", false);
            _client.SetOnOffItem("V401", false);
            _client.SetOnOffItem("V402", false);
            _client.SetOnOffItem("V403", false);
            _client.SetOnOffItem("V404", false);
            _client.SetValveOpening("V102", 0);
            _client.SetPumpControl("P100", 0);
            _client.SetPumpControl("P200", 0);
            _client.SetValveOpening("V104", 0);
        }


        /// <summary>
        /// Start the process sequence with using Task to run multiple threads
        /// </summary>
        /// <param name="i_time">Impreganation time in minutes</param>
        /// <param name="c_time">Cooking time in minutes</param>
        /// <param name="c_pressure">Cooking pressure in hPa</param>
        /// <param name="c_temp">Cooking temperature in Celsius</param>
        public void start_process(int i_time, double c_time, int c_pressure, int c_temp)
        {
            var impreg = new Task(() => process(i_time, c_time, c_pressure, c_temp));
            impreg.Start();
        }


        private void process(int i_time, double c_time, int c_pressure, int c_temp)
        {
            _control = new Control(hold_time, c_pressure, c_temp);
            impregnation(i_time);
            black_liquor_fill();
            white_liquor_fill();
            cooking(c_time, c_pressure, c_temp);
            discharge();
        }


        private void impregnation(int i_time)
        {
            _ui.invoke_sequence_status("impreganation");
            _client.SetOnOffItem("P100_P200_PRESET", true);
            EM2_OP1();
            EM5_OP1();
            EM3_OP2();

            while (_connection.LS_300_plus == false)
            {
            }

            EM3_OP1();

            // Kyllästysaika ja kuluneen ajan seuraaminen stopwachin avulla.
            Stopwatch impreg_clock = new Stopwatch();
            impreg_clock.Start();
            while (impreg_clock.Elapsed.TotalMilliseconds < i_time * 60000)
            {
            }
            impreg_clock.Stop();

            // Pysäytä säie hetkellisesti jotta paineen lasku voidaan nähdä käyttöliittymässä.
            EM2_OP2();
            EM5_OP3();
            EM3_OP6();
            EM3_OP8();


        }

        private void black_liquor_fill()
        {
            _ui.invoke_sequence_status("blackfill");
            EM3_OP2();
            EM5_OP1();
            EM4_OP1();

            while (true)
            {
                if (_connection.LI400_val <= 25) { break; }
            }
            
            EM3_OP6();
            EM5_OP3();
            EM4_OP2();
        }

        private void white_liquor_fill()
        {
            _ui.invoke_sequence_status("whitefill");
            EM3_OP3();
            EM1_OP2();
            while (true)
            {
                if (_connection.LI100_val <= 150)
                {
                    break;
                }
            }
            EM3_OP6();
            EM1_OP4();
        }

        private void cooking(double time, int pressure, double temp)
        {
            _ui.invoke_sequence_status("cooking");
            EM3_OP4();
            EM1_OP1();
            while (true)
            {
                if (_connection.TI300_val <= temp) { break; }
            }
            EM3_OP1();
            EM1_OP2();

            // Aloita keittäminen ja sen tilojen ohjaaminen
            Stopwatch cooking_timer = new Stopwatch();
            cooking_timer.Start();
            while (cooking_timer.Elapsed.TotalMilliseconds <= time * 60000)
            {
                U1_OP1(pressure);
                U1_OP2(temp);
                System.Threading.Thread.Sleep(hold_time); // Hz taajuus säädön ohjaamiselle
            }
            cooking_timer.Stop();

            U1_OP3();
            U1_OP4();
            EM3_OP6();
            EM1_OP4();
            EM3_OP8();
        }

        private void discharge()
        {
            _ui.invoke_sequence_status("discharge");
            EM5_OP2();
            EM3_OP5();
            while (_connection.LS_300_minus)
            {
            }
            EM5_OP4();
            EM3_OP7();
            _ui.invoke_sequence_status("");
            shutdown_process();
        }

        // Add all PFC mini processes as their own methods for the sequence.
        private void EM1_OP1()
        {
            _client.SetValveOpening("V102", 100);
            _client.SetOnOffItem("V304", true);
            _client.SetPumpControl("P100", 100);
            _client.SetOnOffItem("E100", true);
        }


        private void EM1_OP2()
        {
            _client.SetValveOpening("V102", 100);
            _client.SetOnOffItem("V304", true);
            _client.SetPumpControl("P100", 100);
        }

        private void EM1_OP3()
        {
            _client.SetValveOpening("V102", 0);
            _client.SetOnOffItem("V304", false);
            _client.SetPumpControl("P100", 0);
            _client.SetOnOffItem("E100", false);
        }

        private void EM1_OP4()
        {
            _client.SetValveOpening("V102", 0);
            _client.SetOnOffItem("V304", false);
            _client.SetPumpControl("P100", 0);
        }

        private void EM2_OP1()
        {
            _client.SetOnOffItem("V201", true);
        }

        private void EM2_OP2()
        {
            _client.SetOnOffItem("V201", false);
        }

        private void EM3_OP1()
        {
            _client.SetValveOpening("V104", 0);
            _client.SetOnOffItem("V204", false);
            _client.SetOnOffItem("V401", false);
        }


        private void EM3_OP2()
        {
            _client.SetOnOffItem("V204", true);
            _client.SetOnOffItem("V301", true);
        }


        private void EM3_OP3()
        {
            _client.SetOnOffItem("V301", true);
            _client.SetOnOffItem("V401", true);
        }


        private void EM3_OP4()
        {
            _client.SetValveOpening("V104", 100);
            _client.SetOnOffItem("V301", true);
        }


        private void EM3_OP5()
        {
            _client.SetOnOffItem("V204", true);
            _client.SetOnOffItem("V302", true);
        }


        private void EM3_OP6()
        {
            _client.SetValveOpening("V104", 0);
            _client.SetOnOffItem("V204", false);
            _client.SetOnOffItem("V301", false);
            _client.SetOnOffItem("V401", false);
        }


        private void EM3_OP7()
        {
            _client.SetOnOffItem("V302", false);
            _client.SetOnOffItem("V204", false);
        }

        private void EM3_OP8()
        {
            _client.SetOnOffItem("V204", true);
            System.Threading.Thread.Sleep(1000);
            _client.SetOnOffItem("V204", false);
        }


        private void EM4_OP1()
        {
            _client.SetOnOffItem("V404", true);
        }


        private void EM4_OP2()
        {
            _client.SetOnOffItem("V404", false);
        }


        private void EM5_OP1()
        {
            _client.SetOnOffItem("V303", true);
            _client.SetPumpControl("P200", 100);
        }


        private void EM5_OP2()
        {
            _client.SetOnOffItem("V103", true);
            _client.SetOnOffItem("V303", true);
            _client.SetPumpControl("P200", 100);
        }


        private void EM5_OP3()
        {
            _client.SetOnOffItem("V303", false);
            _client.SetPumpControl("P200", 0);
        }


        private void EM5_OP4()
        {
            _client.SetOnOffItem("V103", false);
            _client.SetOnOffItem("V303", false);
            _client.SetPumpControl("P200", 0);
        }


        private void U1_OP1(int pressure)
        {
            try
            {
                lock (_lock_object)
                {
                    int valve_v104 = _control.pressure_control(_connection.PI300_val);
                    _client.SetValveOpening("V104", valve_v104);
                }
            }
            catch (Exception e)
            {
            }
        }


        private void U1_OP2(double temperature)
        {
            try
            {
                lock (_lock_object)
                {
                    bool heater_E100 = _control.temperature_control(_connection.TI300_value);
                    _client.SetOnOffItem("E100", heater_E100);
                }
            }
            catch (Exception e)
            {
            }
        }


        private void U1_OP3()
        {
            _client.SetValveOpening("V104", 0);
        }


        private void U1_OP4()
        {
            _client.SetOnOffItem("E100", false);
        }
    }
}
