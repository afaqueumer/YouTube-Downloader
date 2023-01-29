import streamlit as st 
from pytube import YouTube
import re
import os
from moviepy.editor import AudioFileClip, VideoFileClip
import moviepy.editor as mp



# def add_bg_from_url():
#     st.markdown(
#          f"""
#          <style>
#          .stApp {{
#              background-image: url("https://images.pexels.com/photos/8537029/pexels-photo-8537029.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"); 
#              background-attachment: fixed;
#              background-size: cover
#          }}
#          </style>
#          """,
#          unsafe_allow_html=True
#      )

# add_bg_from_url() 

directory = 'downloads/'

if not os.path.exists(directory):
    os.makedirs(directory)

st.header("YouTube Downloader 📺")
url = st.text_input("", placeholder='Enter the Youtube URL here 👈')

@st.cache(allow_output_mutation=True)
def get_video_data(url):
    v_info = {}
    v_info["yt"] = YouTube(url)
    resolutions = ["720p", "480p", "360p"]
    for r in resolutions:
        prog = v_info["yt"].streams.filter(file_extension='mp4',  progressive=True, resolution=r)
        if len(list(prog))==1:
            v_info["resolution"]=r
            v_info["itag"] = list(prog.filter(resolution=r).itag_index.keys())[0]
            v_info["prog"] = prog
            v_info["stream"] = prog.get_by_itag(v_info["itag"])
            break
    return v_info

@st.cache(allow_output_mutation=True)
def get_adaptive_data(yt):
    adap = yt.streams.filter(file_extension='mp4', adaptive=True, only_video=True)
    adapt_resolutions = []
    video_tags = []
    for i in adap:
        r = re.search(r'(\d+)p', str(i))
        t = re.search("\d\d\d", str(i))
        adapt_resolutions.append(str(i)[r.start():r.end()]) 
        video_tags.append(str(i)[t.start():t.end()])
    return {"resolutions":adapt_resolutions, "itag":video_tags, "streams":adap}
    


if url:
    v_info = get_video_data(url)
    tab1, tab2 = st.tabs(["Basic", "Advanced"])
    
    
    col1, col2 = tab1.columns(2, gap="small")
    col3, col4 = tab2.columns(2, gap="small")
    
    # Tab 1 - Basic (Progressive Download)
  
        
   

    with col1:
        st.image(v_info["yt"].thumbnail_url)
    with col2:
        st.header("Details")
        st.write(f"Title: {v_info['yt'].title}")
        st.write(f"Length: {v_info['yt'].length} sec")
        st.write(f"Resolution: {v_info['resolution']}")
        
          
    basic_file_name = tab1.text_input('__Save as 🎯__', placeholder = v_info['yt'].title, key=1)
    if basic_file_name:        
        if basic_file_name != v_info['yt'].title:
            basic_file_name+=".mp4"
    else:
        basic_file_name = v_info['yt'].title + ".mp4"
    
    prog_but = tab1.button("Download 📥", key=2)
    if prog_but:
        with st.spinner('Downloading...'):
            v_info['stream'].download(output_path="downloads/", filename= basic_file_name)
        st.success('Download Complete', icon="✅")       
        st.balloons()
        
    
        
    with col3:
        st.image(v_info["yt"].thumbnail_url)
    with col4:
        
        adapt_dic = get_adaptive_data(v_info["yt"])       
        
        ad_res = st.selectbox('__Select Resolution__', adapt_dic["resolutions"])
                
        adst = adapt_dic["streams"]       
        vid_stream = adst.get_by_itag(adapt_dic["itag"][adapt_dic["resolutions"].index(ad_res)])
        st.write(f"__Stream_Details__: {vid_stream}")
        # st.write(v_info["yt"].streams.filter(only_audio=True))     
   
    file_name = tab2.text_input('__Save as 🎯__', placeholder = v_info['yt'].title, key=3)
    if file_name:        
        if file_name != v_info['yt'].title:
            file_name+=".mp4"
    else:
        file_name = v_info['yt'].title + ".mp4"
    
    adv_but = tab2.button("Download 📥", key=4)
    if adv_but:
        with st.spinner('Downloading Files...'):
                       
            ad_video =  vid_stream
            ad_audio = v_info["yt"].streams.filter(only_audio=True).first()
            ad_video.download(output_path="temp/", filename= "v.mp4")
            ad_audio.download(output_path="temp/", filename= "a.mp3")
            
        st.success('Files Downloaded', icon="✅")       
        with st.spinner('Merging Files...'):
            inputvideo = "temp/v.mp4"
            inputaudio = "temp/a.mp3"
            video = VideoFileClip(inputvideo)
            audio = AudioFileClip(inputaudio)
            audio = mp.CompositeAudioClip([audio])
            video.audio = audio
            video.write_videofile(filename=f"down.mp4")
         
        st.success('Files Merged - Download Complete', icon="✅")        
        st.balloons()
    
    
    

