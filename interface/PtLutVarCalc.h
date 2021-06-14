#ifndef PtLutVarCalc_h
#define PtLutVarCalc_h

double range_phi_deg(double deg);

double calc_phi_loc_deg_from_glob(double glob, int sector);

int calc_phi_loc_int(double glob, int sector);

int calc_theta_int(double theta, int endcap);

int CalcTrackTheta( const int th1, const int th2, const int th3, const int th4,
                    const int ring1, const int mode, const bool BIT_COMP=false );

void CalcDeltaPhis( int& dPh12, int& dPh13, int& dPh14, int& dPh23, int& dPh24, int& dPh34, int& dPhSign,
		    int& dPhSum4, int& dPhSum4A, int& dPhSum3, int& dPhSum3A, int& outStPh,
		    const int ph1, const int ph2, const int ph3, const int ph4, const int mode, const bool BIT_COMP=false );

void CalcDeltaPhisGEM( int& dPh12, int& dPh13, int& dPh14, int& dPh23, int& dPh24, int& dPh34, int& dPhSign,
                            int& dPhSum4, int& dPhSum4A, int& dPhSum3, int& dPhSum3A, int& outStPh, int& dPhGE11ME11,
                            const int ph1, const int ph2, const int ph3, const int ph4, const int phGEM, const int mode, const bool BIT_COMP=false );

void CalcPhiRun3( int& ph, int ring, int strip_quart_bit, int strip_eight_bit, int station, int endcap, bool useQuartBit, bool useEighthBit);

void CalcDeltaThetas( int& dTh12, int& dTh13, int& dTh14, int& dTh23, int& dTh24, int& dTh34,
		      const int th1, const int th2, const int th3, const int th4, const int mode, const bool BIT_COMP=false );

void ConvertSlopeToRun2Pattern(const int slope, int& pattern);

void ConvertSlopeToRun2Pattern(const int slope1, const int slope2, const int slope3, const int slope4,
                               int& pat1, int& pat2, int& pat3, int& pat4);

void CalcBends( int& bend1, int& bend2, int& bend3, int& bend4,
		const int pat1, const int pat2, const int pat3, const int pat4,
		const int pat1_run3, const int pat2_run3, const int pat3_run3, const int pat4_run3,
		const int dPhSign, const int endcap, const int mode, const bool BIT_COMP=false, const bool isRun2=false );

void CalcSlopes( const int bend, int& slope, const int endcap, const int mode, const bool BIT_COMP, const bool isRun2);

void CalcDeltaSlopes(const int slope1, const int slope2, const int slope3, const int slope4,
                     int& dSlope12, int& dSlope13, int& dSlope14, int& dSlope23, int& dSlope24, int& dSlope34);

void CalcRPCs( int& RPC1, int& RPC2, int& RPC3, int& RPC4, const int mode,
	       const int st1_ring2, const int theta, const bool BIT_COMP=false );

int CalcBendFromPattern( const int pattern, const int endcap, const bool isRun2=false );

int CalcBendFromRun3Pattern( const int pattern, const int endcap );

void CalcDeltaPhiSums( int& dPhSum4, int& dPhSum4A, int& dPhSum3, int& dPhSum3A, int& outStPh,
                       const int dPh12, const int dPh13, const int dPh14, const int dPh23, const int dPh24, const int dPh34 );

#endif
