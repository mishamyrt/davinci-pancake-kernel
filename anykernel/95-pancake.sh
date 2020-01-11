#!/system/bin/sh

#
# Wait for /data to be mounted
#

while ! mountpoint -q /data; do
	sleep 1
done

if ! grep -q Pancake /proc/version; then
	# Remove this init script
	rm -f /data/adb/service.d/95-pancake.sh

	# Abort and do not apply tweaks
	exit 0
fi

#
# Wait for Android to finish booting
#

while [ "$(getprop sys.boot_completed)" != 1 ]; do
	sleep 2
done

echo 1000 > /dev/blkio/blkio.weight
echo 10 > /dev/blkio/background/blkio.weight

sleep 2

echo 8 > /dev/stune/schedtune.boost

echo 1 > /sys/module/printk/parameters/console_suspend
echo 3000 > /proc/sys/vm/dirty_expire_centisecs

# Reduce I/O read-ahead to 64 KiB
echo 64 > /sys/block/sda/queue/read_ahead_kb
echo 64 > /sys/block/sdf/queue/read_ahead_kb

sysctl vm.dirty_ratio=7
sysctl vm.dirty_background_ratio=3
