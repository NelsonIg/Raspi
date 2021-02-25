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
staticNode = findNodeByName(uaClient.Namespace,"MyCar",'-once');
rpm = ones(1,100);
i = 1;
while i < 101 
    rpm(i) = readValue(uaClient, staticNode.Children);
    pause(1);
    i = i+1;
end
figure
plot(rpm);

%% Read and Write Values
clear;
host = '192.168.0.183';
[status, uaClient] = connectOpcua(host);
Car = findNodeByName(uaClient.Namespace, 'Car', '-once');
motor = findNodeByName(Car, 'motor', '-once');
rpm = findNodeByName(Car, 'rpm', '-once');
rpmSet = 300;
step = 0.002;
period = 0.01; % sec
speed = 0.1;
i = 1;
error = 0;
motor.writeValue(0.0);
pause(2);
rpmVals = ones(1,100);
while i<301
    if error < 0
        speed = speed - step
    else
        speed = speed + step
    end
    if speed > 1
        speed = 1;
    end
    if speed < 0
        speed = 0;
    end
    motor.writeValue(speed)
    rpmIs = rpm.readValue();
    rpmVals(i) = rpmIs;
    if rpmIs > -1
        error = rpmSet-rpmIs;
    end
    pause(0.1)
    i = i+1;
end
motor.writeValue(0.0);
figure
plot(rpmVals);
    