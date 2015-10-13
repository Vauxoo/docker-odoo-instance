# docker build -t runbot .
# docker run -d -e POSTGRES_USER=runbot -e POSTGRES_PASSWORD=runbot --name dbrunbot postgres
# docker run -itP --link dbrunbot:dbrunbot runbot

FROM vauxoo/odoo-80-image
MAINTAINER Moises Lopez <moylop260@vauxoo.com>
RUN adduser --home=/home/runbot --disabled-password --gecos "" --shell=/bin/bash runbot
RUN echo 'root:runbot' |chpasswd

RUN mkdir -p /home/runbot/instance/config \
    && mkdir -p /home/runbot/instance/extra_addons \
    && mkdir -p /home/runbot/.ssh \
    && mkdir -p /home/runbot/.local/share/Odoo/filestore \
    && mkdir -p /var/log/supervisor
ADD files/odoo_runbot.conf /home/runbot/instance/config/odoo_runbot.conf
ADD files/entrypoint.sh /entrypoint.sh
ADD files/db_source /home/runbot/.db_source
ADD files/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN chown runbot:runbot -R /home/runbot \
    && chown runbot:runbot /entrypoint.sh

RUN apt-get update && apt-get install nginx \
    && ln -s /usr/sbin/nginx /usr/bin/nginx

# Extra depends: panama-dv for modules vauxoo, t2d for runbot, pyopenssl for security warning
RUN pip install --upgrade git+https://github.com/Vauxoo/panama-dv.git \
    && pip install --upgrade git+https://github.com/vauxoo/travis2docker.git \
    && pip install --upgrade pyopenssl ndg-httpsclient pyasn1

# Install docker in docker
RUN curl -sSL https://get.docker.com/ | sh

# Install ngrok to run fowardporting in developer environment
RUN curl https://dl.ngrok.com/ngrok_2.0.19_linux_amd64.zip -o /tmp/ngrok.zip \
    && unzip -o /tmp/ngrok.zip -d /usr/local/bin/ \
    && rm -rf /tmp/ngrok.zip

USER runbot

# Force home path to fix `supervisor start odoo` print os.expand('~') output: /root/
ENV HOME /home/runbot

RUN echo "source /home/runbot/.db_source" >> /home/runbot/.profile

ENV EXTRA_ADDONS /home/runbot/instance/extra_addons

# Add to known hosts git server
RUN ssh-keyscan github.com > ${HOME}/.ssh/known_hosts \
    && ssh-keyscan launchpad.net >> ${HOME}/.ssh/known_hosts \
    && ssh-keyscan bitbucket.org >> ${HOME}/.ssh/known_hosts \
    && ssh-keyscan gitlab.com >> ${HOME}/.ssh/known_hosts

# Add config basic user to work with git
RUN git config --global user.email "runbot@vauxoo.com" && \
    git config --global user.name "Runbot Vauxoo"

# Clone all repo depends
RUN git clone -b 9.0 https://github.com/odoo/odoo.git ${HOME}/instance/odoo \
    && git clone -b 8.0 https://github.com/OCA/runbot-addons.git ${EXTRA_ADDONS}/runbot-addons \
    && git clone -b master https://github.com/odoo/odoo-extra.git ${EXTRA_ADDONS}/odoo-extra

# Apply patches
#   Patch 8.0 -> 9.0
RUN find ${EXTRA_ADDONS}/odoo-extra/runbot -name res_config_view.xml -exec sed -i 's/base.menu_config/base.menu_administration/g' {} \;

# Finish with root
USER root
RUN usermod -aG docker runbot

# Dev tool
RUN curl http://j.mp/spf13-vim3 -L -o - | sh

# Docker configuration
VOLUME ["/home/runbot/.local/share/Odoo/filestore", "/home/runbot/instance/extra_addons/odoo-extra/runbot/static", "/var/log/supervisor", "/var/lib/docker", "/home/runbot/.ssh"]

# Docker port
EXPOSE 2376

# Odoo instance
EXPOSE 8069 8072 8080 80

CMD /entrypoint.sh
