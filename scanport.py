import nmap
import csv
import argparse
import os


def argument_parser():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', default=False, dest='ip_file', required=True,
                        help='file name of IPs')
    parser.add_argument('-n', default=False, dest='line_number', required=False,
                        help='line no of the Ips file')
    return parser


def save_csv_data(nm_csv, path='.'):
    if os.stat(path + '/output.csv').st_size == 0:
        with open(path + '/output.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Host', 'State', 'Protocol'])
            writer.writerows(nm_csv)
    else:
        with open(path + '/output.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(nm_csv)


def scan_subnet(host="192.168.1.0/24", argument='-sV'):
    nm.scan(hosts=host, arguments=argument)
    print("These are the all host %s " % nm.all_hosts())
    row_list = []
    for host in nm.all_hosts():
        print('Host : %s (%s)' % (host, nm[host].hostname()))
        print('State : %s' % nm[host].state())
        for proto in nm[host].all_protocols():
            print('----------')
            print('Protocol : %s' % proto)
            lport = nm[host][proto].keys()
            row_list.append([host, nm[host].state(), list(lport)])
            save_csv_data(row_list)
        # else:
        #     row_list.append([host, nm[host].state()])
        #     save_csv_data(row_list)

def main():
    global nm
    nm = nmap.PortScanner()
    parser = argument_parser()
    parameters = parser.parse_args()
    filename = parameters.ip_file
    number = parameters.line_number
    counter = 0
    indexing = number if number else 0
    if filename:
        print(filename)
        with open(filename) as f:
            content = f.readlines()
        print(content)
        if int(indexing) > 0:
            print("scanning line from given line number %s " % indexing)
        try:
            for i in content[-int(indexing):]:
                scan_subnet(host=i)
                print(i)
                counter += 1
        except Exception as e:
            print(str(e))
            print("number of element left in the array %s" % (len(content) - counter))

    else:
        print("Invalid choice")
        exit(1)


if __name__ == '__main__':
    main()


















