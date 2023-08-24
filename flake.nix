{
  inputs = {
    nixpkgs = {
      url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    };
    utils = {
      url = "github:numtide/flake-utils";
    };
  };

  outputs = { self, nixpkgs, utils }:
    utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system;  };

        requires = with pkgs; [
          (python311.withPackages(ps: [ ps.pyvips ]))
          vips
        ];
      in
      rec {
        # `nix build`
        packages = (pkgs.lib.mapAttrs' (name: _: 
          pkgs.lib.nameValuePair name (pkgs.stdenv.mkDerivation {
            inherit name;
            version = "master";
            src = ./gfx/${name};
            buildInputs = requires;

            dontCheck = true;
            dontPatch = true;
            dontConfigure = true;

            buildPhase = ''
              python3 ${./tools/compose.py} --use-all --feedback CONCISE . compiled
            '';
            installPhase = ''
              mkdir -p $out
              cp compiled/* $out
              for file in [ "fallback.png" "layering.json" "tileset.txt" ]; do
                [ -f "$file" ] && cp "$file" $out ||:
              done
            '';
          })
        ) (builtins.readDir ./gfx));

        # `nix develop`
        devShell = pkgs.mkShell rec {
          nativeBuildInputs = requires;
        };
      });
}
