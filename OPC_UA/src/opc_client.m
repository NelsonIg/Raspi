%% Example opc ua client
% host should be same as in opc server
% it can take some tries till connection is successful
% all commented values for host work so far


clear;
notConnected = 1;
host = '192.168.0.183';  % 'pi.local';  %'192.168.0.183';

while notConnected
    try
        S = opcuaserverinfo(host);
        uaClient = opcua(S(1));
        notConnected = 0;
    catch
        warning('Try to connect again to opc ua server');
    end
end
%uaClient = opcua('opc.tcp://192.168.0.183:4840/opcua');
connect(uaClient)
staticNode = findNodeByName(uaClient.Namespace,"MyObject",'-once');
readValue(uaClient, staticNode.Children)
