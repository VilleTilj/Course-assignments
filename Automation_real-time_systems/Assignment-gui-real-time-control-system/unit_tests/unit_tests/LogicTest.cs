using gui_app;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using Tuni.MppOpcUaClientLib;

namespace unit_tests
{
    
    
    /// <summary>
    ///This is a test class for LogicTest and is intended
    ///to contain all LogicTest Unit Tests
    ///</summary>
    [TestClass()]
    public class LogicTest
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
        ///A test for YV2:TJ1 shutdown_process
        ///</summary>
        [TestMethod()]
        public void shutdown_processTest()
        {
            MainWindow ui = new MainWindow(); 
            MppClient client = new MppClient(new ConnectionParamsHolder("opc.tcp://127.0.0.1:8087")); 
            ConnectOpcUa connection = new ConnectOpcUa(ui);
            connection.connect("opc.tcp://127.0.0.1:8087");
            object lock_object = new object(); 
            Logic target = new Logic(ui, client, connection, lock_object); 
            target.shutdown_process();
            Assert.AreEqual(ui.E100label.Text, "OFF");
            Assert.AreEqual(ui.V103_label.Text, "OFF");
            Assert.AreEqual(ui.v102label.Text, "0 %");
            Assert.AreEqual(ui.P100label.Text, "0 %");
        }
    }
}
