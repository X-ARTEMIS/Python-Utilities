# pip install speedtest-cli
import speedtest

def test_speed():
    st = speedtest.Speedtest()
    
    # Get the best server based on ping
    st.get_best_server()
    
    # Perform download and upload speed tests
    download_speed = st.download()
    upload_speed = st.upload()
    
    # Convert speeds from bits per second to megabits per second
    download_speed_mbps = download_speed / 1_000_000
    upload_speed_mbps = upload_speed / 1_000_000
    
    return download_speed_mbps, upload_speed_mbps

def main():
    print("Testing network speed...")
    download_speed, upload_speed = test_speed()
    print(f"Download speed: {download_speed:.2f} Mbps")
    print(f"Upload speed: {upload_speed:.2f} Mbps")

if __name__ == "__main__":
    main()
