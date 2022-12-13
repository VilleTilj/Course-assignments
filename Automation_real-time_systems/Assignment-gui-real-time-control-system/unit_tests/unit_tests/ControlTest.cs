using gui_app;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;

namespace unit_tests
{
    
    
    /// <summary>
    ///This is a test class for ControlTest and is intended
    ///to contain all ControlTest Unit Tests
    ///</summary>
    [TestClass()]
    public class ControlTest
    {


        private TestContext testContextInstance;

        /// <summary>
        ///Gets or sets the test context which provides
        ///information about and functionality for the current test run.
        ///</summary>
        public TestContext TestContext
        {
            get
            {
                return testContextInstance;
            }
            set
            {
                testContextInstance = value;
            }
        }

        #region Additional test attributes
        // 
        //You can use the following additional attributes as you write your tests:
        //
        //Use ClassInitialize to run code before running the first test in the class
        //[ClassInitialize()]
        //public static void MyClassInitialize(TestContext testContext)
        //{
        //}
        //
        //Use ClassCleanup to run code after all tests in a class have run
        //[ClassCleanup()]
        //public static void MyClassCleanup()
        //{
        //}
        //
        //Use TestInitialize to run code before running each test
        //[TestInitialize()]
        //public void MyTestInitialize()
        //{
        //}
        //
        //Use TestCleanup to run code after each test has run
        //[TestCleanup()]
        //public void MyTestCleanup()
        //{
        //}
        //
        #endregion


        /// <summary>
        ///A test for Control Constructor
        ///</summary>
        [TestMethod()]
        public void ControlConstructorTest()
        {
            int hold_time = 50; // TODO: Initialize to an appropriate value
            int pressure_setpoint = 100; // TODO: Initialize to an appropriate value
            int temperature_setpoint = 35; // TODO: Initialize to an appropriate value
            Control_Accessor target = new Control_Accessor(hold_time, pressure_setpoint, temperature_setpoint);
            Assert.AreEqual(target._hold_time, 50);
            Assert.AreEqual(target._pressure_setpoint, 100);
            Assert.AreEqual(target._temperature_setpoint, 35);
        }

        /// <summary>
        ///A test for pressure_control
        ///</summary>
        [TestMethod()]
        public void pressure_controlTest()
        {
            int hold_time = 50; 
            int pressure_setpoint = 100; 
            int temperature_setpoint = 35; 
            Control target = new Control(hold_time, pressure_setpoint, temperature_setpoint); 
            double measured_pressure = -200; 
            int value = target.pressure_control(measured_pressure);
            Assert.IsTrue(100 >= value ||value >= 0, "The pressure control value was not in the limits of the valve.");

            double measured_pressure2 = 320;
            int value2 = target.pressure_control(measured_pressure2);
            Assert.IsTrue(100 >= value2 || value2 >= 0, "The pressure control value was not in the limits of the valve.");
  
        }
    }
}
