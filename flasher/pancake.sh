#!/system/bin/sh

# Wait for /data to be mounted
while ! mountpoint -q /data; do
	sleep 1
done

# Remove this script if kernel were changed
if ! grep -q Pancake /proc/version; then
	rm -f /data/adb/service.d/96-pancake.sh
	exit 0
fi

# Wait for /vendor to be mounted
while ! mountpoint -q /vendor; do
	sleep 1
done

if ! mount | grep -q /vendor/etc/msm_irqbalance.conf; then
  # Replace msm_irqbalance.conf
  echo "PRIO=1,1,1,1,1,1,0,0
# arch_timer,arch_mem_timer,arm-pmu,kgsl-3d0
IGNORED_IRQ=19,38,21,332" > /dev/msm_irqbalance.conf
  chmod 644 /dev/msm_irqbalance.conf
  mount --bind /dev/msm_irqbalance.conf /vendor/etc/msm_irqbalance.conf
  chcon "u:object_r:vendor_configs_file:s0" /vendor/etc/msm_irqbalance.conf
  killall msm_irqbalance
  sleep 1
  start vendor.msm_irqbalance
fi

# Wait for Android to finish booting
while [ "$(getprop sys.boot_completed)" != 1 ]; do
	sleep 2
done

# Adjust readahead
find /sys/block/sd* | while read node; do
  echo 128 > "$node/queue/read_ahead_kb"
done

# Reduce big cluster maximum frequency
chmod 644 /sys/devices/system/cpu/cpu6/cpufreq/scaling_max_freq
echo 2169600 > /sys/devices/system/cpu/cpu6/cpufreq/scaling_max_freq
