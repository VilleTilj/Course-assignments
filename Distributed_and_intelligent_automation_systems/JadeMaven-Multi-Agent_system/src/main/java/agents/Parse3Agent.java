/*****************************************************************
 JADE - Java Agent DEvelopment Framework is a framework to develop
 multi-agent systems in compliance with the FIPA specifications.
 Copyright (C) 2000 CSELT S.p.A.

 GNU Lesser General Public License

 This library is free software; you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation,
 version 2.1 of the License.

 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public
 License along with this library; if not, write to the
 Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 Boston, MA  02111-1307, USA.
 *****************************************************************/

package agents;

import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.domain.DFService;
import jade.domain.FIPAAgentManagement.DFAgentDescription;
import jade.domain.FIPAAgentManagement.ServiceDescription;
import jade.domain.FIPAException;
import jade.lang.acl.ACLMessage;
import jade.util.Logger;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;


/**
 * This agent implements a simple Ping Agent that registers itself with the DF and
 * then waits for ACLMessages.
 * If  a REQUEST message is received containing the string "ping" within the content
 * then it replies with an INFORM message whose content will be the string "pong".
 *
 * @author Tiziana Trucco - CSELT S.p.A.
 * @version  $Date: 2010-04-08 13:08:55 +0200 (gio, 08 apr 2010) $ $Revision: 6297 $
 */
public class Parse3Agent extends Agent {

    private Logger myLogger = Logger.getMyLogger(getClass().getName());

    private class WaitPingAndReplyBehaviour extends CyclicBehaviour {

        public WaitPingAndReplyBehaviour(Agent a) {
            super(a);
        }

        public void action() {
            ACLMessage  msg = myAgent.receive();

            if(msg != null){
                ACLMessage reply = msg.createReply();

                if(msg.getPerformative()== ACLMessage.REQUEST){
                    String content = msg.getContent();

                    if ((content != null) ){
                        myLogger.log(Logger.INFO, "Agent "+getLocalName()+" - Received PING Request from "+msg.getSender().getLocalName());
                        reply.setPerformative(ACLMessage.INFORM);

                        //PArse JSON
                        JSONParser parser = new JSONParser();

                        JSONObject jsonObj = new JSONObject();
                        try {
                            jsonObj = (JSONObject) parser.parse(content);

                            String src = (String) jsonObj.get("src");
                            ((JSONArray) jsonObj.get("midPoints")).add(getLocalName());

                            System.out.println(getLocalName()+": Src value"+src);




                        } catch (ParseException e) {
                            e.printStackTrace();
                        }


                        reply.setContent(jsonObj.toJSONString());
                    }
                    else{
                        myLogger.log(Logger.INFO, "Agent "+getLocalName()+" - Unexpected request ["+content+"] received from "+msg.getSender().getLocalName());
                        reply.setPerformative(ACLMessage.REFUSE);
                        reply.setContent("( UnexpectedContent ("+content+"))");
                    }

                }
                else {
                    myLogger.log(Logger.INFO, "Agent "+getLocalName()+" - Unexpected message ["+ACLMessage.getPerformative(msg.getPerformative())+"] received from "+msg.getSender().getLocalName());
                    reply.setPerformative(ACLMessage.NOT_UNDERSTOOD);
                    reply.setContent("( (Unexpected-act "+ACLMessage.getPerformative(msg.getPerformative())+") )");
                }
                send(reply);
            }
            else {
                block();
            }
        }
    } // END of inner class WaitPingAndReplyBehaviour


    protected void setup() {
        // Registration with the DF
        DFAgentDescription dfd = new DFAgentDescription();
        ServiceDescription sd = new ServiceDescription();
        sd.setType("PingAgent");
        sd.setName(getName());
        sd.setOwnership("TILAB");
        dfd.setName(getAID());
        dfd.addServices(sd);

        //PArse JSON
        JSONParser parser = new JSONParser();

        //{"dest":"CONV6","midPoints":["CONV1","CONV2","CONV3"]}
        String testStr="{\"dest\":\"CONV6\",\"midPoints\":[\"CONV1\",\"CONV2\",\"CONV3\"]}";




        try {

            JSONObject jsonObject = (JSONObject) parser.parse(testStr);
            String dest = (String) jsonObject.get("dest");
            System.out.println("Required destination is: "+dest);


            System.out.println("Json object BEFORE adding CONV4 ");
            System.out.println(jsonObject);

            ((JSONArray) jsonObject.get("midPoints")).add("CONV4");
            System.out.println("Json object AFTER adding CONV4 ");
            System.out.println(jsonObject);






        } catch (ParseException e) {
            e.printStackTrace();
        }








        System.out.println("Agent name");
        System.out.println(getLocalName());

        try {
            JSONObject jsonObj = (JSONObject) parser.parse(testStr);

            String dest = (String) jsonObj.get("dest");
            System.out.println("Required destination"+dest);

            System.out.println(jsonObj);

            //Adding midPoint
            ((JSONArray) jsonObj.get("midPoints")).add((String)"CONV4");

            //Modifying an element
            //jsonObj.put("midPoints",midPointsJArr);
            System.out.println("After adding via point");
            System.out.println(jsonObj);

            System.out.println("Converting JSON object to string...");
            String jsonStr=jsonObj.toString();
            System.out.println(jsonStr);

            System.out.println("Number of viaPoints: "+((JSONArray)jsonObj.get("midPoints")).size());


            /*
            //Converting JSONArr to list of strings & printing JSONArray
            List<String> list = new ArrayList<String>();
            System.out.println("******Conveyors in the array!!");
            for(int i = 0; i < midPointsJArr.size(); i++){
                list.add((String)midPointsJArr.get(i));
            }
            */






        } catch (ParseException e) {
            e.printStackTrace();
        }


        try {
            DFService.register(this,dfd);
            WaitPingAndReplyBehaviour PingBehaviour = new  WaitPingAndReplyBehaviour(this);
            addBehaviour(PingBehaviour);
        } catch (FIPAException e) {
            myLogger.log(Logger.SEVERE, "Agent "+getLocalName()+" - Cannot register with DF", e);
            doDelete();
        }
    }
}