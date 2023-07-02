.. _systemd:

What is systemd
===============

Systemd is a commonly used part of many linux distributions to start and control services and other things.

Systemd unit file
+++++++++++++++++

Systemd services are configured by so called unit files. The unit file for the wordclock is called `wordclock.service`
and is linked from `/home/pi/rpi_wordclock/wordclock_config/wordclock.service` to `/etc/systemd/system/wordclock.service`
during the setup, so that the systemd daemon knows it exists::

    sudo ln -s /home/pi/rpi_wordclock/wordclock_config/wordclock.service /etc/systemd/system

The deamon needs to be informed about new or changed unit files by running::

    sudo systemctl daemon-reload

By default, the wordclock unit is configured to restart always after five seconds of waiting, if the software crashed.

.. note:: Since there is only this systemd unit file called `wordclock.service`, the `.service` part can be left out on
  all of the following commands. It is documented this way, since it is technically more accurate.

Common systemd tasks
++++++++++++++++++++

Starting and stopping the wordclock
-----------------------------------

To start the wordclock, run the following command::

    sudo systemctl start wordclock.service


.. note:: Please be aware, that the service will not be started after the next reboot this way.

And to stop the wordclock, run the following command::

    sudo systemctl stop wordclock.service


Enabling and disabling the wordclock
------------------------------------

To start the wordclock on every boot, the unit needs to be enabled. By adding the optional `--now`, systemd will also start it
immediately::

    sudo systemctl enable --now wordclock.service

To disable and stop the wordclock, the command is::

    sudo systemctl disable --now wordclock.service

Check the status of the wordclock unit
--------------------------------------

To check if the service is running and to see more details about it, run::

    sudo systemctl status wordclock.service

Check the output of the wordclock unit
--------------------------------------

If you want to check the output of the wordclock software, you can run::

    sudo journalctl -fu wordclock.service

The optional `f` option will follow the output and the `u` option specifies the unit.
