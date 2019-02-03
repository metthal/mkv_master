# MKV Master

This project was created to quickly:

* Add new audio track encoded with AAC codec (using `libfdk_aac`) in MKVs with only DTS/TrueHD audio tracks.
* Add subtitles into MKV while shifting them (shifting ussported only for SRT format).

The docker image contains:

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
* Custom `mkvm` Python 3 script

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
	docker run --rm --user $(id -u):$(id -g) -v $(realpath .):/opt -w /opt metthal/mkv_master "$@"
}
```

It starts a new container (which is deleted automatically as it terminates) with working directory set to `/opt`. Current directory is mounted as volume to the path `/opt` so all the files that are available in your current directory are available in the container.

Run `mkvm` to see how to use the `mkvm` script.

```
mkvm --help
```


## Disclaimer

This is just a personal project for my own use that I decided to share here. Do what you want with this project (that does not violate the license). Improvements in form of pull requests are appreciated. New features are all DIY.
