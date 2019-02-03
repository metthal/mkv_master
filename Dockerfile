FROM ubuntu:cosmic

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y \
	autoconf automake build-essential git libtool \
	mkvtoolnix nasm pkg-config python3-pip zlib1g-dev

RUN git clone https://git.ffmpeg.org/ffmpeg.git /build/ffmpeg
RUN git clone https://github.com/mstorsjo/fdk-aac.git /build/fdk-aac
RUN git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git /build/nv-codec-headers

RUN cd /build/nv-codec-headers && \
	make install

RUN cd /build/fdk-aac && \
	./autogen.sh && \
	./configure --enable-shared=no --enable-static=yes && \
	make -j$(nproc) install

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
	frei0r-plugins-dev gnutls-dev ladspa-sdk libaom-dev libass-dev \
	libbluray-dev libdrm-dev libgsm1-dev libmp3lame-dev libopencore-amrnb-dev \
	libopencore-amrwb-dev libopenjp2-7-dev libopus-dev libpulse-dev \
	librsvg2-dev libsoxr-dev libspeex-dev libtheora-dev libvo-amrwbenc-dev \
	libvorbis-dev libvpx-dev libx264-dev libx265-dev libxvidcore-dev libzvbi-dev \
	libopenal-dev nvidia-opencl-dev libgcrypt20-dev libcdio-paranoia-dev

RUN  cd /build/ffmpeg && \
	./configure --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libvo-amrwbenc \
		--enable-fontconfig --enable-frei0r --enable-gcrypt --enable-gnutls \
		--enable-ladspa --enable-libaom --enable-libass --enable-libbluray --enable-libcdio \
		--enable-libdrm --enable-libfreetype --enable-libfribidi --enable-libgsm \
		--enable-libmp3lame --enable-nvenc --enable-openal --enable-opencl --enable-opengl \
		--enable-libopenjpeg --enable-libopus --enable-libpulse --enable-librsvg --enable-libsoxr \
		--enable-libspeex --enable-libtheora --enable-libvorbis \
		--enable-libvpx --enable-libx264 --enable-libx265 --enable-libxvid --enable-libzvbi --enable-avfilter \
		--enable-avresample --enable-postproc --enable-pthreads --enable-runtime-cpudetect --enable-gpl \
		--enable-version3 --disable-debug --enable-libfdk-aac --enable-nonfree && \
	make -j$(nproc) install

ADD mkvm /mkvm
RUN chmod +x /mkvm/run.py
RUN pip3 install -r /mkvm/requirements.txt

ENV PATH="/mkvm:${PATH}"
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

ENTRYPOINT ["run.py"]
