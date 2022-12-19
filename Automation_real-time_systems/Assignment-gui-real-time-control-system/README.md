# Cource project
The assignment was to create a real-time automation system using UML2 and C# .NET 4.2 Framework using customer requirements and process diagrams.

## Design
The idea was to follow software design principles similar to MDD (Model driven development). The UML design was implemented based on customer requirements. GUI design was drawn before it was implemented and the architecture principles followed MVC (Model-View-Controller) model.

## Implemented software
- The GUI follows the process drawing of the system. 
- The application is connected to the system simulator using OPC UA client library.
- To control cooking pressure and temperature, simple PI-controller and ON-OFF controller had been implemented.
- The application can be stopped at any time and it goes to Fail safe mode.
- Sequence can be started again after a previous one.
- Unit tests have been implemented. System testing was also done by the developers.
