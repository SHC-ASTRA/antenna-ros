final: prev:
{
  antenna-pkg = final.callPackage ././install/antenna_pkg/share/antenna_pkg/package.nix {};
  ros2-interfaces-pkg = final.callPackage ././install/ros2_interfaces_pkg/share/ros2_interfaces_pkg/package.nix {};
}
