using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

using Tuni.MppOpcUaClientLib;
using UnifiedAutomation.UaBase;
using UnifiedAutomation.UaClient;

namespace gui_app
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    /// 
    public partial class MainWindow : Window
    {

        ConnectOpcUa process_object = null;

        /// <summary>
        /// Mainwindow constructor.
        /// </summary>
        public MainWindow()
        {
            InitializeComponent();

        }


        private void slider1_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            Slider slider = e.OriginalSource as Slider;

            if (slider != null)
            {
                int value = (int)slider.Value;
                c_pressure_label.Text = value.ToString() + " hPa";
            }
        }


        private void c_temp_input_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            Slider slider = e.OriginalSource as Slider;

            if (slider != null)
            {
                int value = (int)slider.Value;
                c_temp_label.Text = value.ToString() + " °C";
            }
        }


        private void cooking_pressure_input_TextChanged(object sender, TextChangedEventArgs e)
        {
            TextBox box = e.OriginalSource as TextBox;

            string text = box.Text;
            foreach (char c in text)
            {
                bool is_number = check_input_val(c);
                if (is_number == false)
                {
                    box.Text = "";
                    imp_label.Text = "0 min";
                    
                }
                else
                {
                    imp_label.Text = text + " min";
                }
            }

        }

        private bool check_input_val(char c)
        {    
           
                if (c < '0' || c > '9')
                {
                    MessageBox.Show("Input must contain time in numbers");
                    return false;
                }
                else
                {
                    return true;
                }

        }


        private void cooking_input_TextChanged(object sender, TextChangedEventArgs e)
        {
            TextBox box = e.OriginalSource as TextBox;

            string text = box.Text;
            foreach (char c in text)
            {
                bool is_number = check_input_val(c);
                if (is_number == false)
                {
                    box.Text = "";
                    c_time_label.Text = "0 min";

                }
                else
                {
                    c_time_label.Text = text + " min";
                }
            }
        }


        private void start_Click(object sender, RoutedEventArgs e)
        {
            // Read the time inputs from the textboxes
            string imp_time_str = new string(imp_label.Text.Where(c => char.IsDigit(c)).ToArray());
            string c_time_str = new string(c_time_label.Text.Where(c => char.IsDigit(c)).ToArray());

            // Make the time inputs as doubles
            int imp_time_float = int.Parse(imp_time_str);
            int c_time_float = int.Parse(c_time_str);

            // Get inputs from the sliders
            string c_pressure_str = new string(c_pressure_label.Text.Where(c => char.IsDigit(c)).ToArray());
            string c_temp_str = new string(c_temp_label.Text.Where(c => char.IsDigit(c)).ToArray());

            // Change the slider text inputs to ints 
            int c_pressure_int = int.Parse(c_pressure_str);
            int c_temp_int = int.Parse(c_temp_str);
            if (check_cooking_input(c_pressure_int, c_temp_int))
            {
                MessageBox.Show("Starting sequence");
                stop_button.IsEnabled = true;
                start.IsEnabled = false;
                process_object.process_logic.start_process(imp_time_float, c_time_float, c_pressure_int, c_temp_int);
            }
            else
            {
                MessageBox.Show("Input parameters are not valid.");
            }
        }

        private bool check_cooking_input(int pressure, int temperature)
        {
            if (pressure < 0 || temperature < 0 || pressure > 350 || temperature > 80)
            {
                return false;
            } 
            else 
            {
                return true;
            }
        }


        private void connect_Click(object sender, RoutedEventArgs e)
        {
            process_object = new ConnectOpcUa(this);
            string url = "opc.tcp://127.0.0.1:8087";
            process_object.connect(url);
            
        }


        private void stop_button_Click(object sender, RoutedEventArgs e)
        {
            start.IsEnabled = false;
            connect_button.IsEnabled = true;
            stop_button.IsEnabled = false;
            process_object.process_logic.shutdown_process();
            change_sequence_status("");
            if (process_object != null)
            {
                // TODO add controll class object
                process_object.process_logic = null;
                process_object.Dispose();
                process_object = null;

            }
            else
            {
                statuslabel.Text = "OFFLINE";
                statuslabel.Foreground = Brushes.Red;
            }
        }

        /// <summary>
        /// Visualizes the connection lost to the ui.
        /// </summary>
        public void connection_offline()
        {
            MessageBox.Show("Connection lost.");
            statuslabel.Text = "OFFLINE";
            statuslabel.Foreground = Brushes.Red;
            connect_button.IsEnabled = true;
            start.IsEnabled = false;
            stop_button.IsEnabled = false;
        }
        

        /// <summary>
        /// Visualizes the connection online to the ui.
        /// </summary>
        public void connection_online()
        {
            statuslabel.Text = "ONLINE";
            statuslabel.Foreground = Brushes.Green;
        }


        /// <summary>
        /// Invokes mainwindow to show PI300 value from another thread. 
        /// </summary>
        /// <param name="value">New PI300 value from simulation</param>
        public void invoke_PI300_value(string value)
        {
            Dispatcher.BeginInvoke((Action)(() => update_PI300_value(value)));
        }


        private void update_PI300_value(string value)
        {
            PI300label.Text = value + "hPa";
        }


        /// <summary>
        /// Invokes mainwindow to show E100 value from another thread. 
        /// </summary>
        /// <param name="value">New E100 value</param>
        public void invoke_E100_value(bool value)
        {
            Dispatcher.BeginInvoke((Action)(() => change_E100_value(value)));
        }


        private void change_E100_value(bool value)
        {
            if (value)
            {
                E100label.Text = "ON";
                E100label.Foreground = Brushes.Green;
            }
            else
            {
                E100label.Text = "OFF";
                E100label.Foreground = Brushes.Red;
            }
        }

        /// <summary>
        /// Shows warning to user with messagebox of LA+100 sensor triggered.
        /// </summary>
        public void trigger_warning()
        {
            MessageBox.Show("WARNING: LA+100 triggered.");
        }


        /// <summary>
        /// Invokes mainwindow to show progressbar values from another thread. 
        /// </summary>
        /// <param name="bar">Name of the progressbar</param>
        /// <param name="value">New value of the bar</param>
        public void invoke_progress_bars(string bar, int value)
        {
            Dispatcher.BeginInvoke((Action)(() => update_pb_Status(bar, value)));
        }


        private void update_pb_Status(string bar, int value)
        {
            if (bar == "LI200")
            {
                LI200_pbar.Value = value;
            }
            if (bar == "LI100")
            {
                LI100_pbar.Value = value;
            }

            if (bar == "LI400")
            {
                LI00_pbar.Value = value;
            }
        }


        /// <summary>
        /// Invokes mainwindow to show LI100 value from another thread. 
        /// </summary>
        /// <param name="status">New LI100 value from simulator</param>
        public void invoke_LI300_plus_status(bool status)
        {
            Dispatcher.BeginInvoke((Action)(() => update_LS300p_status(status)));
        }


        private void update_LS300p_status(bool status)
        {
            textBlock10.Text = "LS+300 " + status.ToString();
        }


        /// <summary>
        /// Invokes mainwindow to show LS300-minus value from another thread. 
        /// </summary>
        /// <param name="status">New LS300-minus value from simulator</param>
        public void invoke_LS300_minus_status(bool status)
        {
            Dispatcher.BeginInvoke((Action)(() => update_LS300m_status(status)));
        }


        private void update_LS300m_status(bool status)
        {
            textBlock13.Text = "LS-300 " + status.ToString();
        }


        /// <summary>
        /// Invokes mainwindow to show pumps value from another thread. 
        /// </summary>
        /// <param name="pump">Name of the pump</param>
        /// <param name="value">New pump value</param>
        public void invoke_pumps(string pump, string value)
        {
            Dispatcher.BeginInvoke((Action)(() => update_pump_value(pump, value)));
        }


        private void update_pump_value(string pump, string value)
        {
            if (pump == "P100")
            {
                P100label.Text = value + " %";
            }
            if (pump == "P200")
            {
                P200label.Text = value + " %";
            }
        }


        /// <summary>
        /// Invokes mainwindow to show T100 value from another thread. 
        /// </summary>
        /// <param name="value">New TI100 value from simulator</param>
        public void change_TI100_value(string value)
        {
            Dispatcher.BeginInvoke((Action)(() => update_TI100_Status(value)));
        }
        

        private void update_TI100_Status(string value)
        {
            TI100label.Text = value + " °C";
        }


        /// <summary>
        /// Invokes mainwindow to show TI300 value from another thread. 
        /// </summary>
        /// <param name="value">New TI300 value from simulator</param>
        public void change_TI300_value(string value)
        {
            Dispatcher.BeginInvoke((Action)(() => update_TI300_Status(value)));
        }


        private void update_TI300_Status(string value)
        {
            TI300label.Text = value + " °C";
        }


        /// <summary>
        /// Invokes mainwindow to show valve value from another thread. 
        /// </summary>
        /// <param name="valve">Name of the valve</param>
        /// <param name="value">New valve value from simulator</param>
        public void invoke_valve_control(string valve, string value)
        {
            Dispatcher.BeginInvoke((Action)(() => set_valve_value(valve, value)));
        }


        private void set_valve_value(string valve, string value)
        {
            if (valve == "v102")
            {
                v102label.Text = value + " %";
            }
            if (valve == "v104")
            {
                v104label.Text = value + " %";
            }
        }


        /// <summary>
        /// Invokes mainwindow to show what sequence is currently on going from another thread. 
        /// </summary>
        /// <param name="sequence">Name of the sequence</param>
        public void invoke_sequence_status(string sequence)
        {
            Dispatcher.BeginInvoke((Action)(() => change_sequence_status(sequence)));
        }


        private void change_sequence_status(string sequence)
        {
            if (sequence == "impreganation")
            {
                impreganation.Background = Brushes.Green;
            }
            else if (sequence == "blackfill")
            {
                impreganation.Background = Brushes.White;
                balckfill.Background = Brushes.Green;
            }
            else if (sequence == "whitefill")
            {
                balckfill.Background = Brushes.White;
                whitefill.Background = Brushes.Green;
            }
            else if (sequence == "cooking")
            {
                whitefill.Background = Brushes.White;
                cooking.Background = Brushes.Green;
            }
            else if (sequence == "discharge")
            {
                cooking.Background = Brushes.White;
                discharge.Background = Brushes.Green;
            }
            else
            {
                impreganation.Background = Brushes.White;
                balckfill.Background = Brushes.White;
                whitefill.Background = Brushes.White;
                cooking.Background = Brushes.White;
                discharge.Background = Brushes.White;
                start.IsEnabled = true;
            }
        }


        /// <summary>
        /// Invokes mainwindow to show valve on off value from another thread. 
        /// </summary>
        /// <param name="valve">Name of the value</param>
        /// <param name="value">New value of the valve from simulator</param>
        public void invoke_valve_onoff(string valve, bool value)
        {
            Dispatcher.BeginInvoke((Action)(() => toggle_valve(valve, value)));
        }


        private void toggle_valve(string valve, bool value)
        {
            string text = null;
            var brush = Brushes.White;
            if (value)
            {
                text = "ON";
                brush = Brushes.Green;
            }
            else
            {
                text = "OFF";
                brush = Brushes.Red;
            }

            if (valve == "v101")
            {
                v101label.Text = text;
                v101label.Foreground = brush;
            }
            if (valve == "v103")
            {
                V103_label.Text = text;
                V103_label.Foreground = brush;
            }
            if (valve == "v201")
            {
                v201label.Text = text;
                v201label.Foreground = brush;
            }
            if (valve == "v202")
            {
                v202label.Text = text;
                v202label.Foreground = brush;
            }
            if (valve == "v203")
            {
                v203label.Text = text;
                v203label.Foreground = brush;
            }
            if (valve == "v204")
            {
                v204label.Text = text;
                v204label.Foreground = brush;
            }
            if (valve == "v301")
            {
                v301label.Text = text;
                v301label.Foreground = brush;
            }
            if (valve == "v302")
            {
                v302label.Text = text;
                v302label.Foreground = brush;
            }
            if (valve == "v303")
            {
                v303label.Text = text;
                v303label.Foreground = brush;
            }
            if (valve == "v304")
            {
                v304label.Text = text;
                v304label.Foreground = brush;
            }
            if (valve == "v401")
            {
                v401label.Text = text;
                v401label.Foreground = brush;
            }
            if (valve == "v402")
            {
                v402label.Text = text;
                v402label.Foreground = brush;
            }
            if (valve == "v403")
            {
                v403label.Text = text;
                v403label.Foreground = brush;
            }
            if (valve == "v404")
            {
                v404label.Text = text;
                v404label.Foreground = brush;
            }
        }
    }
}
