test:
	python3 barber.py --debug --ms ~/astro/cyg2052.ms
bust:
	python3 barber.py --ms ~/astro/G330_HI.avg.ms --pol=0

.PHONY: ao
ao:
	aoflagger -v -column DATA -fields 0 ~/astro/cyg2052.ms
