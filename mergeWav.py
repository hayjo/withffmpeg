import subprocess
import glob

def mergeWav(wavList, outputPath = None):
    """
    ffmpeg wav concatenate 기능을 리스트 텍스트파일 생성 없이 실행
    https://trac.ffmpeg.org/wiki/Concatenate
    wavPathList: list
    outputPath: str, output.wav가 될 경로, 미입력시 폴더명.wav
    """
    if not wavList:
        return None
    if outputPath == None:
        outputPath = "\\".join(wavList[0].split('\\')[:-1]) + ".wav"

    files, filteroption = [], ""
    for path in wavList:
        files = files + ["-i", path]
    for idx in range(len(wavList)):
        filteroption = filteroption + "[" + str(idx) + ":a:0]"
    filteroption = filteroption + "concat=n=" \
                    + str(len(wavList)) + ":v=0:a=1[outa]"
    
    cmd = ["ffmpeg",
        "-hide_banner" ] + files + [
           "-filter_complex",
           "{0}".format(filteroption),
           "-map",
           "[outa]",
           "{0}".format(outputPath)
           ]

    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.communicate()[1].decode('utf-8')

    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, cmd)

def getWavList(dirPath):
    return glob.glob(dirPath + '/*.wav')

mergeWav(getWavList('디렉토리'), '결과 파일명(생략시 폴더명'))