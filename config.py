NAGIP="128.55.218.60"
MMGETSTATE="/usr/lpp/mmfs/bin/mmgetstate"
TMP_DIR="/root/nagios"
DEST_DIR="/var/nagios/corismw"
TMP_MMGETSTATE= TMP_DIR + "/mmgetstate.tmp"
DEST_MMGETSTATE = DEST_DIR + "/mmgetstate.dump"
SSH_ID="/root/nagios/nagios.id"
SSH="/usr/bin/ssh"
SCP="/usr/bin/scp"
MS="corims1"
ELOGIN="cori03"
XTCLI="/opt/cray/hss/default/bin/xtcli"
XTPROCADMIN="/opt/cray/sdb/default/bin/xtprocadmin"
TMP_XTCLI=TMP_DIR+"/xtcli.tmp"
DEST_XTCLI=DEST_DIR+"/xtcli.dump"
TMP_XTPROC=TMP_DIR+"/xtproc.tmp"
DEST_XTPROC=DEST_DIR+"/xtprocadmin.dump"
TMP_SLURM=TMP_DIR+"/slurm.tmp"
DEST_SLURM=DEST_DIR+"/slurm.dump"
DWSTAT="/opt/cray/dws/default/bin/dwstat"
TMP_DWSTAT=TMP_DIR+"/dwstat.tmp"
TMP_DWFRAG=TMP_DIR+"/dwfrag.tmp"
TMP_DWINST=TMP_DIR+"/dwinst.tmp"
TMP_DWSESS=TMP_DIR+"/dwsess.tmp"
TMP_DWACT=TMP_DIR+"/dwact.tmp"
TMP_DWCONF=TMP_DIR+"/dwconf.tmp"
TMP_DWREG=TMP_DIR+"/dwreg.tmp"
DEST_DWSTAT=DEST_DIR+"/dwstat.dump"
DEST_DWFRAG=DEST_DIR+"/dwfrag.dump"
DEST_DWINST=DEST_DIR+"/dwinst.dump"
DEST_DWSESS=DEST_DIR+"/dwsess.dump"
DEST_DWACT=DEST_DIR+"/dwact.dump"
DEST_DWCONF=DEST_DIR+"/dwconf.dump"
DEST_DWREG=DEST_DIR+"/dwreg.dump"
TMP_DF=TMP_DIR+"/boot_df.tmp"
DEST_DF=DEST_DIR+"/boot_df.dump"
TMP_ANSIBLE=TMP_DIR+"/ansible-booted.tmp"
DEST_ANSIBLE=DEST_DIR+"/ansible-booted.dump"
SYS_PREFIX = "cori"
TMP_SDB=TMP_DIR+"/sdb-checks.tmp"
DEST_SDB=DEST_DIR+"/sdb-checks.dump"
TMP_BOOT=TMP_DIR+"/boot-checks.tmp"
DEST_BOOT=DEST_DIR+"/boot-checks.dump"
cron_log="cron_log"
