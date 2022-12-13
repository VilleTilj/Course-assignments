using gui_app;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using Tuni.MppOpcUaClientLib;
using System.Windows.Shapes;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace unit_tests
{
    
    
    /// <summary>
    ///This is a test class for ConnectOpcUaTest and is intended
    ///to contain all ConnectOpcUaTest Unit Tests
    ///</summary>
    [TestClass()]
    public class ConnectOpcUaTest
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
        ///A test for ConnectOpcUa Constructor
        ///</summary>
        [TestMethod()]
        public void ConnectOpcUaConstructorTest()
        {
            MainWindow ui = new MainWindow(); ; 
            ConnectOpcUa target = new ConnectOpcUa(ui);
            Assert.AreNotEqual(target, null);
        }

        /// <summary>
        ///A test for YV1:TJ2 Dispose
        ///</summary>
        [TestMethod()]
        public void DisposeTest()
        {
            MainWindow ui = new MainWindow(); 
            ConnectOpcUa target = new ConnectOpcUa(ui);
            target.Dispose();
            Assert.AreEqual(ui.statuslabel.Text, "OFFLINE");
            Assert.AreEqual(ui.statuslabel.Foreground, Brushes.Red);    
        }


        /// <summary>
        ///A test for YV1:TJ3 connect
        ///</summary>
        [TestMethod()]
        public void connectTest()
        {
            MainWindow ui = new MainWindow(); 
            ConnectOpcUa target = new ConnectOpcUa(ui); 
            string sim_url = "opc.tcp://127.0.0.1:8087";
            target.connect(sim_url);
            Assert.AreEqual(ui.statuslabel.Text,"ONLINE");
            Assert.AreEqual(ui.statuslabel.Foreground, Brushes.Green);
        }
    }
}
