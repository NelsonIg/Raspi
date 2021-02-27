function [out, status] = read_opc_server(inp)
    notConnected = inp;
    host = '127.0.0.1'
    if notConnected
        S = opcuaserverinfo(host);
        uaClient = opcua(S(1));
        connect(uaClient);
    end
    notConnected = 0;
   opcObject = findNodeByName(uaClient.Namespace,"MyObject",'-once');
   opcVar = findNodeByName(opcObject, 'MyVariable', '-once');
   out = opcVar.readValue();
   status = noConnected
end