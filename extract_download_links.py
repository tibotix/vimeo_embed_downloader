import requests
import re
import sys

usage = f"""Usage: python3 {sys.argv[0]} <video_id> <referrer_url>

where video_id is the 9 digit number in the embed link url (https://player.vimeo.com/video/123456789),
and referrer_url is the url in which the video is embedded (https://example.com).

Example: python3 {sys.argv[0]} 123456789 https://example.com"""

def get_download_links(video_id, referrer):
    r = requests.get(f"https://player.vimeo.com/video/{video_id!s}", headers={"Referer": referrer})
    if not r.ok or "mp4" not in r.text:
        raise RuntimeError(f"Could not find video for video_id: {video_id!s}")
    links = re.findall(r"\"([^\"]*?\.mp4)\"", r.text)
    if len(links) == 0:
        raise RuntimeError("Could not extract download links")
    return links

def main():
    if len(sys.argv) != 3:
        print(usage)
        return 1
    video_id = sys.argv[1]
    referrer = sys.argv[2]

    try:
        links = get_download_links(video_id, referrer)
        print(f"[+] Download links: {links!s}")
        return 0
    except RuntimeError as e:
        print(f"[!] Failed: {e!s}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
