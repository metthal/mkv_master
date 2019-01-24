# MKV Master

This project was created to quickly add new audio track encoded with AAC codec (using `libfdk_aac`) in MKVs with only DTS/TrueHD audio tracks.

The docker image contains:

* `mediainfo` built from git
* `libfdk_aac` built from git
* `ffmpeg` built from git with these options:
```
--enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libvo-amrwbenc --enable-fontconfig --enable-frei0r --enable-gcrypt
--enable-gnutls --enable-ladspa --enable-libaom --enable-libass --enable-libbluray --enable-libcdio --enable-libdrm --enable-libfreetype
--enable-libfribidi --enable-libgsm --enable-libmp3lame --enable-nvenc --enable-openal --enable-opencl --enable-opengl --enable-libopenjpeg
--enable-libopus --enable-libpulse --enable-librsvg --enable-libsoxr --enable-libspeex --enable-libtheora --enable-libvorbis
--enable-libvpx --enable-libx264 --enable-libx265 --enable-libxvid --enable-libzvbi --enable-avfilter --enable-avresample --enable-postproc
--enable-pthreads --enable-runtime-cpudetect --enable-gpl --enable-version3 --disable-debug --enable-libfdk-aac --enable-nonfree
```
* Custom `mkv_master` Python 3 script

## Installation

If you just want to use `mkv_master` you can pull the existing docker image from Docker Hub.

```
docker pull metthal/mkv_master
```

or you can build it yourself

```
docker build -t mkv_master .
```

## Usage

I advise you to put this in your `.bashrc`

```
mkvm() {
	docker run --rm --user $(id -u):$(id -g) -v $(realpath .):/opt metthal/mkv_master mkv_master "$@"
}
```

Script `mkv_master` sets the current working directory to `/opt` and this one-liner mounts your current directory to `/opt` inside Docker container. So you can refer to files in your current directory inside the Docker container with the same relative paths. Just run

```
mkvm --help
```

to see how to use the `mkv_master` script.

## Disclaimer

Do what you want with this project. Improvements in form of pull requests are appreciated. New features are all DIY.
