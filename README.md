# 🩺 URL Health Monitor - PyQt GUI (Dockerized)

This is a desktop application to monitor the health of multiple URLs using a graphical user interface (GUI) built with PySide6 (Qt for Python). The app is fully containerized using Docker and runs on Windows with X11 forwarding via VcXsrv.

---

## 🚀 Features

- Enter and monitor multiple URLs.
- View HTTP response status and latency.
- Auto-refresh last 5 URLs every 10 seconds.
- Built using Python, PySide6, and requests.
- Works from a Docker container with GUI support on Windows.

---

## 🧰 Requirements (on your Windows system)

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [VcXsrv](https://sourceforge.net/projects/vcxsrv/) (X11 server to show GUI)
- Git Bash, PowerShell, or CMD

---

## 📦 How to Download and Run

```Docker command
docker pull shivamsingh484/urlhealth:latest
docker run -it --rm -e DISPLAY=host.docker.internal:0.0 urlhealth-01




