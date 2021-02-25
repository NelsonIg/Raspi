function [status, uaClient] = connectOpcua(host)
    notConnected = 1;
    while notConnected
        try
            S = opcuaserverinfo(host);
            uaClient = opcua(S(1));
            connect(uaClient)
            notConnected = 0;
        catch
            warning('Try to connect again to opc ua server');
            warning('Host:', host);
        end
    end
    status = 1;
end