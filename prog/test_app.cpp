#include <iostream>
#include <fstream>
#include <string>
#include <sys/socket.h>
#include <netinet/in.h>
using namespace std;

int write_to_file(const string file_name, const string text) {
  ofstream f(file_name);
  if (f.is_open()){
    f << text;
    f.close();
  }
  else {
    cerr << "Could not open " << file_name << " for write" <<  endl;
    return 1;
  }
  return 0;
}

int create_socket(int domain, int type , int protocol) {
  int socket_fd;
  int opt = 1;

  if ((socket_fd = socket(domain, type, protocol)) == 0) {
    cerr << "couldn't create a socket" << endl;
    return 1;
  }
  if (setsockopt(socket_fd, SOL_SOCKET,
		 SO_REUSEADDR | SO_REUSEPORT, &opt,
		 sizeof(opt))) {
    cerr << "Couldn't bind to socket" << endl;
    return 1;
  }
  return 0;
}


int  main(void)
{
  int err = 0;
  // Fail the systemd service if atleast one of test fails
  if (write_to_file("/home/user/file", "TEST") != 0) { 
    cout << "Couldn't write to /home directory. Check  ProtectHome directive" << endl;
    err++;
  }

  if (write_to_file("/usr/file", "TEST") != 0) {
    cout << "Couldn't write to /usr directory. Check ProtectSystem directive" << endl;
    err++;
  }

  if (create_socket(AF_INET, SOCK_STREAM, 0) != 0) {
    cout << "Couldn't create socket for AF_INET. Check RestrictAddressFamilies" << endl;
    err++;
  }

  return err; 
}
