#include "open62541.h"

#include <signal.h>
#include <stdlib.h>

static volatile UA_Boolean running = true;


//  catches the signal (interrupt) the program receives when
// the operating systems tries to close it.
// Then sets global variable running to false
static void stopHandler(int sig) {
    UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND, "received ctrl-c");
    running = false;
}

int main(void) {
    signal(SIGINT, stopHandler);
    signal(SIGTERM, stopHandler);

    UA_Server *server = UA_Server_new();
    UA_ServerConfig_setDefault(UA_Server_getConfig(server));
    // Run the Server
    // Internally, the server then uses timeouts to schedule regular tasks.
    // Between the timeouts, the server listens on the network layer for incoming messages.
    UA_StatusCode retval = UA_Server_run(server, &running);

    UA_Server_delete(server);
    return retval == UA_STATUSCODE_GOOD ? EXIT_SUCCESS : EXIT_FAILURE;
}
