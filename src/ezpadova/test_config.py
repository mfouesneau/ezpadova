import pytest
from .config import validate_query_parameter, configuration

def test_validate_query_parameter():
    # Base configuration
    base_config = configuration['defaults'].copy()

    # Valid configuration
    validate_query_parameter(**base_config)

    # Test invalid age range
    invalid_age_config = base_config.copy()
    invalid_age_config['isoc_agelow'] = 1e11
    with pytest.raises(ValueError, match='Lower age must be less than upper age. .*'):
        validate_query_parameter(**invalid_age_config)

    # Test invalid log age range
    invalid_log_age_config = base_config.copy()
    invalid_log_age_config['isoc_lagelow'] = 10.15
    with pytest.raises(ValueError, match='Lower log age must be less than upper log age.'):
        validate_query_parameter(**invalid_log_age_config)

    # Test invalid Z range
    invalid_z_config = base_config.copy()
    invalid_z_config['isoc_zlow'] = 0.1
    with pytest.raises(ValueError, match='Lower Z must be less than upper Z.'):
        validate_query_parameter(**invalid_z_config)

    # Test invalid [M/H] range
    invalid_met_config = base_config.copy()
    invalid_met_config['isoc_metlow'] = 0.5
    with pytest.raises(ValueError, match=r'Lower \[M/H\] must be less than upper \[M/H\]. Got 0.5 and 0.3 instead.'):
        validate_query_parameter(**invalid_met_config)

    # Test invalid photometric system file
    invalid_photsys_config = base_config.copy()
    invalid_photsys_config['photsys_file'] = 'invalid_photsys'
    with pytest.raises(ValueError, match='Invalid photometric system file: invalid_photsys'):
        validate_query_parameter(**invalid_photsys_config)

    # Test invalid IMF file
    invalid_imf_config = base_config.copy()
    invalid_imf_config['imf_file'] = 'invalid_imf'
    with pytest.raises(ValueError, match='Invalid IMF file: invalid_imf'):
        validate_query_parameter(**invalid_imf_config)

    # Test invalid track_parsec
    invalid_track_parsec_config = base_config.copy()
    invalid_track_parsec_config['track_parsec'] = 'invalid_track'
    with pytest.raises(ValueError, match='Invalid isochrone kind: invalid_track'):
        validate_query_parameter(**invalid_track_parsec_config)

    # Test invalid track_omegai
    invalid_track_omegai_config = base_config.copy()
    invalid_track_omegai_config['track_omegai'] = 1.0
    with pytest.raises(ValueError, match='Invalid initial rotation velocity. Must be between 0 and 0.99. Found 1.0 instead.'):
        validate_query_parameter(**invalid_track_omegai_config)

    # Test invalid track_colibri
    invalid_track_colibri_config = base_config.copy()
    invalid_track_colibri_config['track_colibri'] = 'invalid_colibri'
    with pytest.raises(ValueError, match='Invalid isochrone kind: invalid_colibri'):
        validate_query_parameter(**invalid_track_colibri_config)

    # Test invalid dust_sourceC
    invalid_dust_sourceC_config = base_config.copy()
    invalid_dust_sourceC_config['dust_sourceC'] = 'invalid_dustC'
    with pytest.raises(ValueError, match='Invalid dust source: invalid_dustC'):
        validate_query_parameter(**invalid_dust_sourceC_config)

    # Test invalid dust_sourceM
    invalid_dust_sourceM_config = base_config.copy()
    invalid_dust_sourceM_config['dust_sourceM'] = 'invalid_dustM'
    with pytest.raises(ValueError, match='Invalid dust source: invalid_dustM'):
        validate_query_parameter(**invalid_dust_sourceM_config)

    # Test invalid extinction_coeff
    invalid_extinction_coeff_config = base_config.copy()
    invalid_extinction_coeff_config['extinction_coeff'] = 'invalid_coeff'
    with pytest.raises(ValueError, match='Invalid extinction coefficient: invalid_coeff'):
        validate_query_parameter(**invalid_extinction_coeff_config)

    # Test invalid extinction_curve
    invalid_extinction_curve_config = base_config.copy()
    invalid_extinction_curve_config['extinction_curve'] = 'invalid_curve'
    with pytest.raises(ValueError, match='Invalid extinction curve: invalid_curve'):
        validate_query_parameter(**invalid_extinction_curve_config)

    # Test invalid kind_LPV
    invalid_kind_LPV_config = base_config.copy()
    invalid_kind_LPV_config['kind_LPV'] = 'invalid_LPV'
    with pytest.raises(ValueError, match='Invalid LPV kind: invalid_LPV'):
        validate_query_parameter(**invalid_kind_LPV_config)

    # Test invalid photsys_version
    invalid_photsys_version_config = base_config.copy()
    invalid_photsys_version_config['photsys_version'] = 'invalid_version'
    with pytest.raises(ValueError, match='Invalid photometric system version: invalid_version'):
        validate_query_parameter(**invalid_photsys_version_config)