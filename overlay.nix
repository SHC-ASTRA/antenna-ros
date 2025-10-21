final: prev:
{
  antenna-pkg = final.callPackage ././src/antenna_pkg/package.nix {};
  astra-msgs = final.callPackage ././src/astra_msgs/package.nix {};
}
