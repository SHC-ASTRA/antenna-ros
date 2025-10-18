final: prev:
{
  antenna-pkg = final.callPackage ././src/antenna_pkg/package.nix {};
  ros2-interfaces-pkg = final.callPackage ././src/ros2_interfaces_pkg/package.nix {};
}
