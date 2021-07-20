
# DSSynth_template for creating new synths

	>> conda activate DSSynth_template
	>> python dsgenerator/generate.py --configfile config_file.json --outputpath testDataset

# Jupyter notebook for exploring synth

>> pip install jupyter

>> python3.8 -m ipykernel install --user --name DSSynth_template

>> jupyter notebook

>> Select *popTexture-notebook.ipynb* in the browser interface

## Reinstall dssynth modules (still testing)

>> pip install -r requirements.txt --src '.'

# Sample template 

The DSsynth template includes a Pop texture as sample template file for creating new synthesizers.

