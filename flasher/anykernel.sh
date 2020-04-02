# AnyKernel3 Ramdisk Mod Script
# osm0sis @ xda-developers

## AnyKernel setup
# begin properties
properties() { '
kernel.string=Pancake Kernel by mishamyrt @ myrt.co
do.devicecheck=1
do.modules=0
do.systemless=1
do.cleanup=1
do.cleanuponabort=0
device.name1=davinci
device.name2=davinciin
device.name3=
device.name4=
device.name5=
supported.versions=
supported.patchlevels=
'; } # end properties

# shell variables
block=/dev/block/bootdevice/by-name/boot;
is_slot_device=0;
ramdisk_compression=auto;
postboot_script=/data/adb/service.d/96-pancake.sh;

## AnyKernel methods (DO NOT CHANGE)
# import patching functions/variables - see for reference
. tools/ak3-core.sh;

## AnyKernel file attributes
# set permissions/ownership for included ramdisk files
set_perm_recursive 0 0 755 644 $ramdisk/*;
set_perm_recursive 0 0 750 750 $ramdisk/init* $ramdisk/sbin;

mountpoint -q /data && {
  # Install second-stage late init script
  mkdir -p /data/adb/service.d
  cp ./pancake.sh $postboot_script
  chmod +x $postboot_script
} || ui_print 'Data is not mounted; some tweaks will be missing'

## AnyKernel install
dump_boot;
write_boot;
## end install
