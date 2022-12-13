using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace gui_app
{
    /// <summary>
    /// Class to control the cooking temperature and pressure using E100 heater and V104 valve.
    /// </summary>
    class Control
    {
        private readonly int _hold_time = 0;
        private readonly double _pressure_setpoint = 0;
        private readonly int _temperature_setpoint = 0;
        private int _valve_control = 0;
        private bool _heater_control = false;
        private readonly double _igain = 0.4;
        private readonly double _pgain = -0.3;
        private double cumsum_error = 0;
        private int _prevent_overshoot = 0;


        /// <summary>
        /// Control class constructor.
        /// </summary>
        /// <param name="hold_time">Discrete time system sample time</param>
        /// <param name="pressure_setpoint">User entered pressure value for the cooking process.</param>
        /// <param name="temperature_setpoint">User entered temperature value for the cooking process.</param>
        public Control(int hold_time, int pressure_setpoint, int temperature_setpoint)
        {
            _hold_time = hold_time;
            _pressure_setpoint = pressure_setpoint;
            _temperature_setpoint = temperature_setpoint;
            _valve_control = 0;
            _heater_control = false;
            
        }


        /// <summary>
        /// Control the process pressure.
        /// </summary>
        /// <param name="measured_pressure">Measured pressure.</param>
        /// <returns>Valve control value</returns>
        public int pressure_control(double measured_pressure)
        {
            if (measured_pressure < 0)
            {
                return _valve_control;
            }
            
            double error = _pressure_setpoint - measured_pressure;

            // PI-controller
            double control = _pgain * error + _igain * cumsum_error;
            cumsum_error += _hold_time/1000 * error;


            int round_control = Convert.ToInt32(Math.Round(control));

            if (_valve_control + round_control < 0)
            {
                _valve_control = 0;
            }
            else if (_valve_control + round_control > 100)
            {
                _valve_control = 100;
            }
            else
            {
                _valve_control += round_control;
            }

            return _valve_control;

        }


        /// <summary>
        /// COntrol cooking temperature.
        /// </summary>
        /// <param name="measured_temperature">Measured cooking temperature.</param>
        /// <returns>Heater on off value</returns>
        public bool temperature_control(double measured_temperature)
        {
            if (_prevent_overshoot < 20 && measured_temperature > _temperature_setpoint - 0.5 && _temperature_setpoint < 40)
            {
                _prevent_overshoot = _prevent_overshoot + 1;
                _heater_control = false;
            }
            else if (measured_temperature < _temperature_setpoint)
            {
                _heater_control = true;
            } 
            else
            {
                _heater_control = false;
            } 
            return _heater_control;
        }
    }
}
