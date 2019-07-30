// Up-to-date with current "master" branch

std::vector<TString> ints = {{
    "evt_run", "evt_LS", "evt_BX",
    "nHits", "nHitsCSC", "nHitsRPC", "nHitsBX0", "nHitsCSCBX0", "nHitsRPCBX0",
    "nSimHits", "nSimHitsCSC", "nSimHitsRPC", "nSimHitsBX0", "nSimHitsCSCBX0", "nSimHitsRPCBX0",
    "nSegs", "nSegsBX0",
    "nTracks", "nTracksBX0",
    "nUnpTracks", "nUnpTracksBX0",
    "nRecoMuons", "nRecoMuonsFwd", "nRecoMuonsTrig", "nRecoMuonsTrigCen",
    "nRecoPairs", "nRecoPairsFwd",
    // "nGenMuons",
  }};

std::vector<TString> longs = {{
    "evt_event", "evt_orbit"
  }};

std::vector<TString> vFlt = {{
    "hit_eta", "hit_theta", "hit_phi", "hit_phi_loc",
    "hit_eta_sim", "hit_theta_sim", "hit_phi_sim",
    "sim_hit_eta", "sim_hit_theta", "sim_hit_phi", "sim_hit_phi_loc",

    "seg_chi2", "seg_time", "seg_eta", "seg_theta", "seg_phi", "seg_globX", "seg_globY", "seg_globZ",
    "seg_locX", "seg_locY", "seg_dirX", "seg_dirY", "seg_dirZ", "seg_bend_theta", "seg_bend_phi",

    "trk_pt", "trk_eta", "trk_theta", "trk_phi", "trk_phi_loc",
    "trk_dR_match_dEta", "trk_dR_match_dPhi", "trk_dR_match_dR",
    "trk_unp_match_dEta", "trk_unp_match_dPhi", "trk_unp_match_dR",

    "unp_trk_pt", "unp_trk_eta", "unp_trk_theta", "unp_trk_phi", "unp_trk_phi_loc",
    "unp_trk_dR_match_dEta", "unp_trk_dR_match_dPhi", "unp_trk_dR_match_dR",
    "unp_trk_emu_match_dEta", "unp_trk_emu_match_dPhi", "unp_trk_emu_match_dR",

    "reco_pt", "reco_eta", "reco_eta_St1", "reco_eta_St2", 
    "reco_theta", "reco_theta_St1", "reco_theta_St2",
    "reco_phi", "reco_phi_St1", "reco_phi_St2",
    "reco_dR_match_emu_dEta", "reco_dR_match_emu_dPhi", "reco_dR_match_emu_dR",
    "reco_dR_match_unp_dEta", "reco_dR_match_unp_dPhi", "reco_dR_match_unp_dR",
    "reco_iso", "reco_d0_BS", "reco_dZ_BS", "reco_d0_PV", "reco_dZ_PV",
    "reco_trig_dR",

    "recoPair_p", "recoPair_pt", "recoPair_pz", "recoPair_mass",
    "recoPair_eta", "recoPair_theta", "recoPair_phi",
    "recoPair_dR", "recoPair_dEta", "recoPair_dTheta", "recoPair_dPhi",
    "recoPair_dR_St1", "recoPair_dEta_St1", "recoPair_dTheta_St1", "recoPair_dPhi_St1",
    "recoPair_dR_St2", "recoPair_dEta_St2", "recoPair_dTheta_St2", "recoPair_dPhi_St2",

    // "mu_pt", "mu_eta", "mu_theta", "mu_phi",
  }};

std::vector<TString> vInt = {{
    "hit_eta_int", "hit_theta_int", "hit_phi_int", "hit_endcap", "hit_sector", "hit_sector_index", "hit_station",
    "hit_ring", "hit_CSC_ID", "hit_chamber", "hit_FR", "hit_pattern", "hit_quality", "hit_roll", "hit_subsector",
    "hit_isCSC", "hit_isRPC", "hit_valid", "hit_BX", "hit_strip", "hit_strip_hi", "hit_strip_low", "hit_wire", "hit_neighbor",
    "hit_match_iSimHit", "hit_sim_match_exact", "hit_match_iSeg", "hit_match_iSeg2", "hit_match_nSegs", "hit_seg_match_unique",

    "sim_hit_eta_int", "sim_hit_theta_int", "sim_hit_phi_int", "sim_hit_endcap", "sim_hit_sector", "sim_hit_sector_index",
    "sim_hit_station", "sim_hit_ring", "sim_hit_CSC_ID", "sim_hit_chamber", "sim_hit_FR", "sim_hit_pattern", "sim_hit_quality",
    "sim_hit_alct_quality", "sim_hit_clct_quality", "sim_hit_roll", "sim_hit_subsector", "sim_hit_isCSC", "sim_hit_isRPC",
    "sim_hit_valid", "sim_hit_BX", "sim_hit_strip", "sim_hit_strip_hi", "sim_hit_strip_low", "sim_hit_wire", "sim_hit_neighbor",
    "sim_hit_match_iHit", "sim_hit_match_exact",

    "seg_endcap", "seg_ring", "seg_station", "seg_chamber", "seg_sector", "seg_CSC_ID",
    "seg_nRecHits", "seg_wire_max", "seg_wire_min", "seg_strip_max", "seg_strip_min",
    "seg_match_iHit", "seg_match_iHit2", "seg_match_nHits", "seg_hit_match_unique",
	
    "trk_pt_int", "trk_eta_int", "trk_theta_int", "trk_phi_int", "trk_BX", "trk_endcap",
    "trk_sector", "trk_sector_index", "trk_mode", "trk_mode_CSC", "trk_mode_RPC", "trk_mode_neighbor",
    "trk_qual", "trk_charge", "trk_nHits", "trk_nRPC", "trk_nNeighbor", "trk_dBX", "trk_dPhi_int", "trk_dTheta_int",
    "trk_dR_match_iReco", "trk_dR_match_iReco2", "trk_dR_match_nReco", "trk_dR_match_nRecoSoft", "trk_dR_match_unique",
    "trk_unp_match_iTrk", "trk_unp_match_iTrk2", "trk_unp_match_dBX", "trk_unp_match_unique", "trk_unp_match_exact",

    "unp_trk_pt_int", "unp_trk_eta_int", "unp_trk_theta_int", "unp_trk_phi_int", "unp_trk_BX","unp_trk_endcap",
    "unp_trk_sector", "unp_trk_sector_index", "unp_trk_mode", "unp_trk_mode_CSC", "unp_trk_mode_RPC", "unp_trk_mode_neighbor",
    "unp_trk_qual", "unp_trk_charge", "unp_trk_nHits", "unp_trk_nRPC", "unp_trk_nNeighbor", "unp_trk_found_hits",
    "unp_trk_dBX", "unp_trk_dPhi_int", "unp_trk_dTheta_int",
    "unp_trk_dR_match_iReco", "unp_trk_dR_match_iReco2", "unp_trk_dR_match_nReco", "unp_trk_dR_match_nRecoSoft", "unp_trk_dR_match_unique",
    "unp_trk_emu_match_iTrk", "unp_trk_emu_match_iTrk2", "unp_trk_emu_match_dBX", "unp_trk_emu_match_unique", "unp_trk_emu_match_exact",

    "reco_ID_soft", "reco_ID_loose", "reco_ID_medium", "reco_ID_tight",
    "reco_ID_PF", "reco_ID_tracker", "reco_ID_stand", "reco_ID_global",
    "reco_ID_station", "reco_ID_nStations", "reco_charge",
    "reco_dR_match_emu_iTrk", "reco_dR_match_emu_iTrk2", "reco_dR_match_emu_nTrk", "reco_dR_match_emu_unique",
    "reco_dR_match_unp_iTrk", "reco_dR_match_unp_iTrk2", "reco_dR_match_unp_nTrk", "reco_dR_match_unp_unique",
    "reco_trig_ID",

    "recoPair_iReco1", "recoPair_iReco2",

    // "mu_charge"
  }};

std::vector<TString> vvInt = {{
    "trk_iHit",
    "unp_trk_iHit"
  }};


// Maps from branch names to branch contents
std::map<TString, int> mInts;
std::map<TString, long long> mLongs;
std::map<TString, std::vector<float>* > mVFlt;
std::map<TString, std::vector<int>* > mVInt;
std::map<TString, std::vector<std::vector<int> >* > mVVInt;


// Fill maps with empty contents for each branch name
inline void InitializeMaps() {
  for (auto & str : ints)  mInts .insert( std::pair<TString, int>(str, 0) );
  for (auto & str : longs) mLongs.insert( std::pair<TString, long long>(str, 0) );
  for (auto & str : vFlt)  { std::vector<float>* vFltTmp = new std::vector<float>();
    mVFlt .insert( std::pair<TString, std::vector<float>* >(str, vFltTmp) ); }
  for (auto & str : vInt)  { std::vector<int>* vIntTmp = new std::vector<int>();
    mVInt .insert( std::pair<TString, std::vector<int>* >(str, vIntTmp) ); }
  for (auto & str : vvInt) { std::vector< std::vector<int> >* vvIntTmp = new std::vector< std::vector<int> >();
    mVVInt.insert( std::pair<TString, std::vector<std::vector<int> >* >(str, vvIntTmp) ); }
}


// Set branch addresses for the TChain
inline void SetBranchAddresses(TChain* this_chain) {
  for (auto & str : ints)  this_chain->SetBranchAddress( str, &mInts .at(str) );
  for (auto & str : longs) this_chain->SetBranchAddress( str, &mLongs.at(str) );
  for (auto & str : vFlt)  this_chain->SetBranchAddress( str, &mVFlt .at(str) );
  for (auto & str : vInt)  this_chain->SetBranchAddress( str, &mVInt .at(str) );
  for (auto & str : vvInt) this_chain->SetBranchAddress( str, &mVVInt.at(str) );
}


// Return the value of a variable corresponding to a string
inline long long I(TString str) {
  if      ( mInts.find(str)  != mInts.end() )
    return (long long) mInts.at(str);
  else if ( mLongs.find(str) != mLongs.end() )
    return mLongs.at(str);
  else { std::cout << "\nString '" << str << "' not found in mInts ('ints') or mLongs ('longs')." << std::endl; 
    throw std::invalid_argument(""); }
};
inline float F(TString str, int idx) {
  if ( mVFlt.find(str) != mVFlt.end() )
    if ( mVFlt.at(str)->size() > idx )
      return mVFlt.at(str)->at(idx);
    else { std::cout << "\nVector '" << str << "' has " << mVFlt.at(str)->size() << " elements, not " << idx+1 << "." << std::endl; 
      throw std::invalid_argument(""); }
  else { std::cout << "\nString '" << str << "' not found in mVFlt ('vFlt')." << std::endl; 
    throw std::invalid_argument(""); }
};
inline int I(TString str, int idx) {
  if ( mVInt.find(str) != mVInt.end() )
    if ( mVInt.at(str)->size() > idx )
      return mVInt.at(str)->at(idx);
    else { std::cout << "\nVector '" << str << "' has " << mVInt.at(str)->size() << " elements, not " << idx+1 << "." << std::endl; 
      throw std::invalid_argument(""); }
  else { std::cout << "\nString '" << str << "' not found in mVInt ('vInt')." << std::endl; 
    throw std::invalid_argument(""); }
};
inline int I(TString str, int idx, int jdx) {
  if ( mVVInt.find(str) != mVVInt.end() )
    if ( mVVInt.at(str)->size() > idx )
      if ( mVVInt.at(str)->at(idx).size() > jdx )
	return mVVInt.at(str)->at(idx).at(jdx);
      else { std::cout << "\nVector '" << str << "' at " << idx << " has " << mVVInt.at(str)->at(idx).size() << " elements, not " << jdx+1 << "." << std::endl; 
	throw std::invalid_argument(""); }
    else { std::cout << "\nVector '" << str << "' has " << mVVInt.at(str)->size() << " elements, not " << idx+1 << "." << std::endl; 
      throw std::invalid_argument(""); }
  else { std::cout << "\nString '" << str << "' not found in mVVInt ('vvInt')." << std::endl; 
    throw std::invalid_argument(""); }
};
inline std::vector<float>* VF(TString str) {
  if ( mVFlt.find(str) != mVFlt.end() )
    return mVFlt.at(str);
  else { std::cout << "\nString '" << str << "' not found in mVFlt ('vFlt')." << std::endl; 
    throw std::invalid_argument(""); }
};
inline std::vector<int>* VI(TString str) {
  if ( mVInt.find(str) != mVInt.end() )
    return mVInt.at(str);
  else { std::cout << "\nString '" << str << "' not found in mVInt ('vInt')." << std::endl; 
    throw std::invalid_argument(""); }
};
inline std::vector<int> VI(TString str, int idx) {
  if ( mVVInt.find(str) != mVVInt.end() )
    if ( mVVInt.at(str)->size() > idx )
      return mVVInt.at(str)->at(idx);
    else { std::cout << "\nVector '" << str << "' has " << mVVInt.at(str)->size() << " elements, not " << idx+1 << "." << std::endl; 
      throw std::invalid_argument(""); }
  else { std::cout << "\nString '" << str << "' not found in mVVInt ('vvInt')." << std::endl; 
    throw std::invalid_argument(""); }
};
inline std::vector< std::vector<int> >* VVI(TString str) {
  if ( mVVInt.find(str) != mVVInt.end() )
    return mVVInt.at(str);
  else { std::cout << "\nString '" << str << "' not found in mVVInt ('vvInt')." << std::endl; 
    throw std::invalid_argument(""); }
};
