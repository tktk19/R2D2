package main

import (
	"bufio"
	"fmt"
	"github.com/jacobsa/go-serial/serial"
	"net/http"
	"time"
)

func openSerial(b []byte) ([]byte, bool, error) {
	options := serial.OpenOptions{
		PortName:        "/dev/ttyACM0",
		BaudRate:        9600,
		DataBits:        8,
		StopBits:        1,
		MinimumReadSize: 4,
	}
	port, err := serial.Open(options)
	if err != nil {
		panic(err)
	}
	defer port.Close()

	port.Write(b)
	if err != nil {
		panic(err)
	}

	time.Sleep(1000000)

	reader := bufio.NewReaderSize(port, 4096)
	return reader.ReadLine()
}

func indexHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "show")
}

func captureHander(w http.ResponseWriter, r *http.Request) {
	b, _, err := openSerial([]byte("c\r\n"))
	if err != nil {
		panic(err)
	}
	fmt.Fprintf(w, string(b))
}

func playHandler(w http.ResponseWriter, r *http.Request) {
	b, _, err := openSerial([]byte("p\r\n"))
	if err != nil {
		panic(err)
	}
	fmt.Fprintf(w, string(b))
}

func main() {
	http.HandleFunc("/", indexHandler)
	http.HandleFunc("/capture", captureHander)
	http.HandleFunc("/play", playHandler)

	http.ListenAndServe(":8000", nil)
}
