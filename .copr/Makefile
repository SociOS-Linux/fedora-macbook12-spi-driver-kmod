srpm:
	dnf -y install rpmdevtools fedpkg wget
	wget https://github.com/roadrunner2/macbook12-spi-driver/archive/3f56ce0d33c47de921db77c3c9829ddc0e26ac9d.tar.gz
	fedpkg --release=f30 srpm
	cp *.src.rpm $(outdir)
