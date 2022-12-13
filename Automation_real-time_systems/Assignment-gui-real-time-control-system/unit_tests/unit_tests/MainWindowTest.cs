using gui_app;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.Windows.Markup;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Shapes;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace unit_tests
{
    
    
    /// <summary>
    ///This is a test class for MainWindowTest and is intended
    ///to contain all MainWindowTest Unit Tests
    ///</summary>
    [TestClass()]
    public class MainWindowTest
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
        ///A test for YV1:TJ_1 input values
        ///</summary>
        [TestMethod()]
        [DeploymentItem("gui-app.exe")]
        public void check_input_valTest()
        {
            MainWindow_Accessor target = new MainWindow_Accessor();
            char value1 = '.';
            bool result = target.check_input_val(value1);
            Assert.AreEqual(result, false);

            char value2 = '4';
            bool result2 = target.check_input_val(value2);
            Assert.AreEqual(result2, true);

            char value3 = 'h';
            bool result3 = target.check_input_val(value3);
            Assert.AreEqual(result3, false);
        }

        /// <summary>
        ///A test for YV1:TJ_1 input values
        ///</summary>
        [TestMethod()]
        [DeploymentItem("gui-app.exe")]
        public void check_cookign_input_valTest()
        {
            MainWindow_Accessor target = new MainWindow_Accessor();
            int c_press1 = 120;
            int c_temp1 = 30;
            bool result = target.check_cooking_input(c_press1, c_temp1);
            Assert.AreEqual(result, true);

            int c_press2 = -1;
            int c_temp2 = 23;
            bool result2 = target.check_cooking_input(c_press2, c_temp2);
            Assert.AreEqual(result2, false);

            int c_press3 = 120;
            int c_temp3 = 400;
            bool result3 = target.check_cooking_input(c_press3, c_temp3);
            Assert.AreEqual(result3, false);
        }

        /// <summary>
        ///A test for YV1:TJ_2 E100 value in simulator 
        ///</summary>
        [TestMethod()]
        [DeploymentItem("gui-app.exe")]
        public void change_E100_valueTest()
        {
            MainWindow_Accessor target = new MainWindow_Accessor(); 
            bool value = false; 
            target.change_E100_value(value);
            Assert.AreEqual(target.E100label.Text, "OFF");
            Assert.AreNotEqual(target.E100label.Text, "ON");
        }


        /// <summary>
        ///A test for YV1:TJ_2 update_TI300_value
        ///</summary>
        [TestMethod()]
        public void update_TI300_valueTest()
        {
            MainWindow_Accessor target = new MainWindow_Accessor(); 
            string value = "20.0";
            target.update_TI300_Status(value);
            Assert.AreEqual(target.TI300label.Text, value + " °C"); 
        }

        /// <summary>
        ///A test for YV1:TJ_2 change_sequence_status
        ///</summary>
        [TestMethod()]
        [DeploymentItem("gui-app.exe")]
        public void change_sequence_statusTest()
        {
            MainWindow_Accessor target = new MainWindow_Accessor();
            string sequence = "cooking"; 
            target.change_sequence_status(sequence);
            Assert.AreEqual(target.cooking.Background, Brushes.Green);
            Assert.AreEqual(target.impreganation.Background, Brushes.White);
            Assert.AreEqual(target.balckfill.Background, Brushes.White);
            Assert.AreEqual(target.whitefill.Background, Brushes.White);
            Assert.AreEqual(target.discharge.Background, Brushes.White);
        }



        /// <summary>
        ///A test for YV1:TJ_2 connection_offline
        ///</summary>
        [TestMethod()]
        public void connection_offlineTest()
        {
            MainWindow_Accessor target = new MainWindow_Accessor();
            target.connection_offline();
            Assert.AreEqual(target.statuslabel.Text,"OFFLINE");
            Assert.AreEqual(target.statuslabel.Foreground, Brushes.Red);
        }

        /// <summary>
        ///A test for YV1:TJ_2 connection_online
        ///</summary>
        [TestMethod()]
        public void connection_onlineTest()
        {
            MainWindow_Accessor target = new MainWindow_Accessor(); 
            target.connection_online();
            Assert.AreEqual(target.statuslabel.Text, "ONLINE");
            Assert.AreEqual(target.statuslabel.Foreground, Brushes.Green);
        }

  


        /// <summary>
        ///A test for YV1:TJ_2 invoke_E100_value
        ///</summary>
        [TestMethod()]
        public void invoke_E100_valueTest()
        {
            MainWindow_Accessor target = new MainWindow_Accessor();
            bool value = false; 
            target.invoke_E100_value(value);
            Assert.AreEqual(target.E100label.Text, "OFF");
        }



        /// <summary>
        ///A test for YV1:TJ_2 update_PI300_value
        ///</summary>
        [TestMethod()]
        public void update_PI300_valueTest()
        {
            MainWindow_Accessor target = new MainWindow_Accessor();
            string value = "88";
            target.update_PI300_value(value);
            Assert.AreEqual(target.PI300label.Text, value + "hPa");
        }

        /// <summary>
        ///A test forY V1:TJ_2 set_valve_control
        ///</summary>
        [TestMethod()]
        public void set_valve_controlTest()
        {
            MainWindow_Accessor target = new MainWindow_Accessor(); 
            string valve = "v102"; 
            string value = "25"; // TODO: Initialize to an appropriate value
            target.set_valve_value(valve, value);
            Assert.AreEqual(value + " %", target.v102label.Text);
        }

        /// <summary>
        ///A test for YV1:TJ_2toggle_valve
        ///</summary>
        [TestMethod()]
        [DeploymentItem("gui-app.exe")]
        public void toggle_valveTest()
        {
            MainWindow_Accessor target = new MainWindow_Accessor(); 
            string valve = "v103";
            bool value = false; 
            target.toggle_valve(valve, value);
            Assert.AreEqual(target.V103_label.Text, "OFF");
            Assert.AreEqual(target.V103_label.Foreground, Brushes.Red);
        }

        /// <summary>
        ///A test for YV1:TJ_2 update_LS300m_status
        ///</summary>
        [TestMethod()]
        [DeploymentItem("gui-app.exe")]
        public void update_LS300m_statusTest()
        {
            MainWindow_Accessor target = new MainWindow_Accessor(); 
            bool status = false;
            target.update_LS300m_status(status);
            Assert.AreEqual(target.textBlock13.Text, "LS-300 False");
        }


        /// <summary>
        ///A test for YV1:TJ_2 update_pb_Status
        ///</summary>
        [TestMethod()]
        [DeploymentItem("gui-app.exe")]
        public void update_pb_StatusTest()
        {
            MainWindow_Accessor target = new MainWindow_Accessor(); 
            string bar = "LI200"; 
            int value = 146;
            target.update_pb_Status(bar, value);
            Assert.AreEqual(target.LI200_pbar.Value, 146);
        }

        /// <summary>
        ///A test for YV1:TJ_2 update_pump_value
        ///</summary>
        [TestMethod()]
        [DeploymentItem("gui-app.exe")]
        public void update_pump_valueTest()
        {
            MainWindow_Accessor target = new MainWindow_Accessor();
            string pump = "P100"; 
            string value = "40"; 
            target.update_pump_value(pump, value);
            Assert.AreEqual(target.P100label.Text, "40" + " %");
        }
    }
}
