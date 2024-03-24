from IPython.display import Javascript
from google.colab import output
from base64 import b64decode
from IPython.display import Javascript
from google.colab import output
from base64 import b64decode

def voicerecorder(filename='audio.mp4', duration=5):
    # JavaScript to prompt user for audio recording
    print("Starting the recording")
    RECORD_AUDIO_JS = """
    const sleep  = time => new Promise(resolve => setTimeout(resolve, time))
    const b2text = blob => new Promise(resolve => {
      const reader = new FileReader()
      reader.onloadend = e => resolve(e.srcElement.result)
      reader.readAsDataURL(blob)
    })
    async function record(duration) {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      let chunks = []
      mediaRecorder.ondataavailable = e => chunks.push(e.data)
      mediaRecorder.start()
      await sleep(duration)
      mediaRecorder.stop()
      await sleep(1000)
      stream.getAudioTracks()[0].stop()
      return new Blob(chunks)
    }
    """

    display(Javascript(RECORD_AUDIO_JS + f"""
    record({duration * 1000}).then(blob => {{
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.style.display = 'none'
      a.href = url
      a.download = 'temp_audio.webm'
      document.body.appendChild(a)
      a.click()
      fetch(url)
        .then(response => response.blob())
        .then(blob => {{
          const reader = new FileReader()
          reader.readAsDataURL(blob)
          reader.onloadend = function() {{
            const base64data = reader.result
            google.colab.kernel.invokeFunction('notebook.RecordAudio', [base64data], {{}})
          }}
        }}
      )
    }})
    """))

    # Handler to save audio file on server side
    def _voicerecorder(base64_audio_data):
        audio_data = b64decode(base64_audio_data.split(',')[1])
        with open(filename, 'wb') as f:
            f.write(audio_data)
        print(f"Audio recording saved as {filename}")

    output.register_callback('notebook.RecordAudio', _voicerecorder)

# Example usage
voicerecorder(duration=5)  # Record for 10 seconds


!ffmpeg -i audio.webm -strict experimental audio.mp4

