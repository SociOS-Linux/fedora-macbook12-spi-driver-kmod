srpm:
	dnf -y install rpmdevtools fedpkg wget
	wget https://github.com/roadrunner2/macbook12-spi-driver/archive/ddfbc7733542b8474a0e8f593aba91e06542be4f.tar.gz
	fedpkg --release=f32 srpm
	cp *.src.rpm $(outdir)
