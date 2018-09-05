#set the base image
FROM jmacey/ngl
# Dockerfile author / maintainer 
MAINTAINER Jon Macey  <jmacey@bournemouth.ac.uk> 
# Set some arguments for finding the nvidia drivers
# Setup  Home
WORKDIR /home/ncca
ENV HOME /home/ncca
ENV QT_QPA_PLATFORM_PLUGIN_PATH /opt/qt/plugins
ENV LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/ncca/NGL/lib:/opt/qt/lib
# add qt to path
ENV PATH=${PATH}:/opt/qt/bin
RUN git clone --depth 1 https://github.com:/NCCA/SimpleNGL && \
cd SimpleNGL && qmake && make -j 4 
RUN set +H && echo -e "#!/bin/bash \n cd /home/ncca/SimpleNGL \n ./SimpleNGL" >run.sh && \
chmod +x run.sh
# set default command
ENTRYPOINT ["/bin/bash","-c","/home/ncca/run.sh"]
