package edu.vanderbilt.riaps.ide.contentassist.antlr.internal;

// Hack: Use our own Lexer superclass by means of import. 
// Currently there is no other way to specify the superclass for the lexer.
import org.eclipse.xtext.ide.editor.contentassist.antlr.internal.Lexer;


import org.antlr.runtime.*;
import java.util.Stack;
import java.util.List;
import java.util.ArrayList;

@SuppressWarnings("all")
public class InternalDatatypesLexer extends Lexer {
    public static final int T__50=50;
    public static final int T__19=19;
    public static final int T__15=15;
    public static final int T__16=16;
    public static final int T__17=17;
    public static final int T__18=18;
    public static final int T__12=12;
    public static final int T__13=13;
    public static final int T__14=14;
    public static final int T__51=51;
    public static final int RULE_ID=4;
    public static final int T__26=26;
    public static final int T__27=27;
    public static final int T__28=28;
    public static final int RULE_INT=6;
    public static final int T__29=29;
    public static final int T__22=22;
    public static final int RULE_ML_COMMENT=8;
    public static final int T__23=23;
    public static final int T__24=24;
    public static final int T__25=25;
    public static final int T__20=20;
    public static final int T__21=21;
    public static final int RULE_STRING=7;
    public static final int RULE_SL_COMMENT=9;
    public static final int T__37=37;
    public static final int T__38=38;
    public static final int T__39=39;
    public static final int T__33=33;
    public static final int T__34=34;
    public static final int T__35=35;
    public static final int T__36=36;
    public static final int EOF=-1;
    public static final int T__30=30;
    public static final int T__31=31;
    public static final int RULE_ANNOTATION_STRING=5;
    public static final int T__32=32;
    public static final int RULE_WS=10;
    public static final int RULE_ANY_OTHER=11;
    public static final int T__48=48;
    public static final int T__49=49;
    public static final int T__44=44;
    public static final int T__45=45;
    public static final int T__46=46;
    public static final int T__47=47;
    public static final int T__40=40;
    public static final int T__41=41;
    public static final int T__42=42;
    public static final int T__43=43;

    // delegates
    // delegators

    public InternalDatatypesLexer() {;} 
    public InternalDatatypesLexer(CharStream input) {
        this(input, new RecognizerSharedState());
    }
    public InternalDatatypesLexer(CharStream input, RecognizerSharedState state) {
        super(input,state);

    }
    public String getGrammarFileName() { return "InternalDatatypes.g"; }

    // $ANTLR start "T__12"
    public final void mT__12() throws RecognitionException {
        try {
            int _type = T__12;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:11:7: ( 'Int8' )
            // InternalDatatypes.g:11:9: 'Int8'
            {
            match("Int8"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__12"

    // $ANTLR start "T__13"
    public final void mT__13() throws RecognitionException {
        try {
            int _type = T__13;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:12:7: ( 'UInt8' )
            // InternalDatatypes.g:12:9: 'UInt8'
            {
            match("UInt8"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__13"

    // $ANTLR start "T__14"
    public final void mT__14() throws RecognitionException {
        try {
            int _type = T__14;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:13:7: ( 'Int16' )
            // InternalDatatypes.g:13:9: 'Int16'
            {
            match("Int16"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__14"

    // $ANTLR start "T__15"
    public final void mT__15() throws RecognitionException {
        try {
            int _type = T__15;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:14:7: ( 'UInt16' )
            // InternalDatatypes.g:14:9: 'UInt16'
            {
            match("UInt16"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__15"

    // $ANTLR start "T__16"
    public final void mT__16() throws RecognitionException {
        try {
            int _type = T__16;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:15:7: ( 'Int32' )
            // InternalDatatypes.g:15:9: 'Int32'
            {
            match("Int32"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__16"

    // $ANTLR start "T__17"
    public final void mT__17() throws RecognitionException {
        try {
            int _type = T__17;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:16:7: ( 'UInt32' )
            // InternalDatatypes.g:16:9: 'UInt32'
            {
            match("UInt32"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__17"

    // $ANTLR start "T__18"
    public final void mT__18() throws RecognitionException {
        try {
            int _type = T__18;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:17:7: ( 'Int64' )
            // InternalDatatypes.g:17:9: 'Int64'
            {
            match("Int64"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__18"

    // $ANTLR start "T__19"
    public final void mT__19() throws RecognitionException {
        try {
            int _type = T__19;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:18:7: ( 'UInt64' )
            // InternalDatatypes.g:18:9: 'UInt64'
            {
            match("UInt64"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__19"

    // $ANTLR start "T__20"
    public final void mT__20() throws RecognitionException {
        try {
            int _type = T__20;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:19:7: ( 'Boolean' )
            // InternalDatatypes.g:19:9: 'Boolean'
            {
            match("Boolean"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__20"

    // $ANTLR start "T__21"
    public final void mT__21() throws RecognitionException {
        try {
            int _type = T__21;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:20:7: ( 'String' )
            // InternalDatatypes.g:20:9: 'String'
            {
            match("String"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__21"

    // $ANTLR start "T__22"
    public final void mT__22() throws RecognitionException {
        try {
            int _type = T__22;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:21:7: ( 'Float' )
            // InternalDatatypes.g:21:9: 'Float'
            {
            match("Float"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__22"

    // $ANTLR start "T__23"
    public final void mT__23() throws RecognitionException {
        try {
            int _type = T__23;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:22:7: ( 'Double' )
            // InternalDatatypes.g:22:9: 'Double'
            {
            match("Double"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__23"

    // $ANTLR start "T__24"
    public final void mT__24() throws RecognitionException {
        try {
            int _type = T__24;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:23:7: ( 'ByteBuffer' )
            // InternalDatatypes.g:23:9: 'ByteBuffer'
            {
            match("ByteBuffer"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__24"

    // $ANTLR start "T__25"
    public final void mT__25() throws RecognitionException {
        try {
            int _type = T__25;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:24:7: ( 'package' )
            // InternalDatatypes.g:24:9: 'package'
            {
            match("package"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__25"

    // $ANTLR start "T__26"
    public final void mT__26() throws RecognitionException {
        try {
            int _type = T__26;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:25:7: ( 'import' )
            // InternalDatatypes.g:25:9: 'import'
            {
            match("import"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__26"

    // $ANTLR start "T__27"
    public final void mT__27() throws RecognitionException {
        try {
            int _type = T__27;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:26:7: ( '.' )
            // InternalDatatypes.g:26:9: '.'
            {
            match('.'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__27"

    // $ANTLR start "T__28"
    public final void mT__28() throws RecognitionException {
        try {
            int _type = T__28;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:27:7: ( '*' )
            // InternalDatatypes.g:27:9: '*'
            {
            match('*'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__28"

    // $ANTLR start "T__29"
    public final void mT__29() throws RecognitionException {
        try {
            int _type = T__29;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:28:7: ( '<**' )
            // InternalDatatypes.g:28:9: '<**'
            {
            match("<**"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__29"

    // $ANTLR start "T__30"
    public final void mT__30() throws RecognitionException {
        try {
            int _type = T__30;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:29:7: ( '**>' )
            // InternalDatatypes.g:29:9: '**>'
            {
            match("**>"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__30"

    // $ANTLR start "T__31"
    public final void mT__31() throws RecognitionException {
        try {
            int _type = T__31;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:30:7: ( 'typeCollection' )
            // InternalDatatypes.g:30:9: 'typeCollection'
            {
            match("typeCollection"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__31"

    // $ANTLR start "T__32"
    public final void mT__32() throws RecognitionException {
        try {
            int _type = T__32;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:31:7: ( '{' )
            // InternalDatatypes.g:31:9: '{'
            {
            match('{'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__32"

    // $ANTLR start "T__33"
    public final void mT__33() throws RecognitionException {
        try {
            int _type = T__33;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:32:7: ( '}' )
            // InternalDatatypes.g:32:9: '}'
            {
            match('}'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__33"

    // $ANTLR start "T__34"
    public final void mT__34() throws RecognitionException {
        try {
            int _type = T__34;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:33:7: ( 'version' )
            // InternalDatatypes.g:33:9: 'version'
            {
            match("version"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__34"

    // $ANTLR start "T__35"
    public final void mT__35() throws RecognitionException {
        try {
            int _type = T__35;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:34:7: ( 'messageCollection' )
            // InternalDatatypes.g:34:9: 'messageCollection'
            {
            match("messageCollection"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__35"

    // $ANTLR start "T__36"
    public final void mT__36() throws RecognitionException {
        try {
            int _type = T__36;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:35:7: ( 'key' )
            // InternalDatatypes.g:35:9: 'key'
            {
            match("key"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__36"

    // $ANTLR start "T__37"
    public final void mT__37() throws RecognitionException {
        try {
            int _type = T__37;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:36:7: ( 'major' )
            // InternalDatatypes.g:36:9: 'major'
            {
            match("major"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__37"

    // $ANTLR start "T__38"
    public final void mT__38() throws RecognitionException {
        try {
            int _type = T__38;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:37:7: ( 'minor' )
            // InternalDatatypes.g:37:9: 'minor'
            {
            match("minor"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__38"

    // $ANTLR start "T__39"
    public final void mT__39() throws RecognitionException {
        try {
            int _type = T__39;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:38:7: ( 'array' )
            // InternalDatatypes.g:38:9: 'array'
            {
            match("array"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__39"

    // $ANTLR start "T__40"
    public final void mT__40() throws RecognitionException {
        try {
            int _type = T__40;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:39:7: ( 'of' )
            // InternalDatatypes.g:39:9: 'of'
            {
            match("of"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__40"

    // $ANTLR start "T__41"
    public final void mT__41() throws RecognitionException {
        try {
            int _type = T__41;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:40:7: ( 'typedef' )
            // InternalDatatypes.g:40:9: 'typedef'
            {
            match("typedef"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__41"

    // $ANTLR start "T__42"
    public final void mT__42() throws RecognitionException {
        try {
            int _type = T__42;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:41:7: ( 'is' )
            // InternalDatatypes.g:41:9: 'is'
            {
            match("is"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__42"

    // $ANTLR start "T__43"
    public final void mT__43() throws RecognitionException {
        try {
            int _type = T__43;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:42:7: ( 'struct' )
            // InternalDatatypes.g:42:9: 'struct'
            {
            match("struct"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__43"

    // $ANTLR start "T__44"
    public final void mT__44() throws RecognitionException {
        try {
            int _type = T__44;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:43:7: ( 'extends' )
            // InternalDatatypes.g:43:9: 'extends'
            {
            match("extends"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__44"

    // $ANTLR start "T__45"
    public final void mT__45() throws RecognitionException {
        try {
            int _type = T__45;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:44:7: ( 'enumeration' )
            // InternalDatatypes.g:44:9: 'enumeration'
            {
            match("enumeration"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__45"

    // $ANTLR start "T__46"
    public final void mT__46() throws RecognitionException {
        try {
            int _type = T__46;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:45:7: ( ',' )
            // InternalDatatypes.g:45:9: ','
            {
            match(','); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__46"

    // $ANTLR start "T__47"
    public final void mT__47() throws RecognitionException {
        try {
            int _type = T__47;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:46:7: ( '=' )
            // InternalDatatypes.g:46:9: '='
            {
            match('='); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__47"

    // $ANTLR start "T__48"
    public final void mT__48() throws RecognitionException {
        try {
            int _type = T__48;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:47:7: ( 'map' )
            // InternalDatatypes.g:47:9: 'map'
            {
            match("map"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__48"

    // $ANTLR start "T__49"
    public final void mT__49() throws RecognitionException {
        try {
            int _type = T__49;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:48:7: ( 'to' )
            // InternalDatatypes.g:48:9: 'to'
            {
            match("to"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__49"

    // $ANTLR start "T__50"
    public final void mT__50() throws RecognitionException {
        try {
            int _type = T__50;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:49:7: ( ']' )
            // InternalDatatypes.g:49:9: ']'
            {
            match(']'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__50"

    // $ANTLR start "T__51"
    public final void mT__51() throws RecognitionException {
        try {
            int _type = T__51;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:50:7: ( '[' )
            // InternalDatatypes.g:50:9: '['
            {
            match('['); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "T__51"

    // $ANTLR start "RULE_ANNOTATION_STRING"
    public final void mRULE_ANNOTATION_STRING() throws RecognitionException {
        try {
            int _type = RULE_ANNOTATION_STRING;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:4445:24: ( '@' ( 'a' .. 'z' | '-' )+ ( ' ' | '\\t' )* ':' ( '\\\\' ( 'b' | 't' | 'n' | 'f' | 'r' | 'u' | '\"' | '\\'' | '\\\\' ) | ( '\\\\*' | '\\\\@' ) | ~ ( ( '\\\\' | '*' | '@' ) ) )* )
            // InternalDatatypes.g:4445:26: '@' ( 'a' .. 'z' | '-' )+ ( ' ' | '\\t' )* ':' ( '\\\\' ( 'b' | 't' | 'n' | 'f' | 'r' | 'u' | '\"' | '\\'' | '\\\\' ) | ( '\\\\*' | '\\\\@' ) | ~ ( ( '\\\\' | '*' | '@' ) ) )*
            {
            match('@'); 
            // InternalDatatypes.g:4445:30: ( 'a' .. 'z' | '-' )+
            int cnt1=0;
            loop1:
            do {
                int alt1=2;
                int LA1_0 = input.LA(1);

                if ( (LA1_0=='-'||(LA1_0>='a' && LA1_0<='z')) ) {
                    alt1=1;
                }


                switch (alt1) {
            	case 1 :
            	    // InternalDatatypes.g:
            	    {
            	    if ( input.LA(1)=='-'||(input.LA(1)>='a' && input.LA(1)<='z') ) {
            	        input.consume();

            	    }
            	    else {
            	        MismatchedSetException mse = new MismatchedSetException(null,input);
            	        recover(mse);
            	        throw mse;}


            	    }
            	    break;

            	default :
            	    if ( cnt1 >= 1 ) break loop1;
                        EarlyExitException eee =
                            new EarlyExitException(1, input);
                        throw eee;
                }
                cnt1++;
            } while (true);

            // InternalDatatypes.g:4445:46: ( ' ' | '\\t' )*
            loop2:
            do {
                int alt2=2;
                int LA2_0 = input.LA(1);

                if ( (LA2_0=='\t'||LA2_0==' ') ) {
                    alt2=1;
                }


                switch (alt2) {
            	case 1 :
            	    // InternalDatatypes.g:
            	    {
            	    if ( input.LA(1)=='\t'||input.LA(1)==' ' ) {
            	        input.consume();

            	    }
            	    else {
            	        MismatchedSetException mse = new MismatchedSetException(null,input);
            	        recover(mse);
            	        throw mse;}


            	    }
            	    break;

            	default :
            	    break loop2;
                }
            } while (true);

            match(':'); 
            // InternalDatatypes.g:4445:62: ( '\\\\' ( 'b' | 't' | 'n' | 'f' | 'r' | 'u' | '\"' | '\\'' | '\\\\' ) | ( '\\\\*' | '\\\\@' ) | ~ ( ( '\\\\' | '*' | '@' ) ) )*
            loop4:
            do {
                int alt4=4;
                int LA4_0 = input.LA(1);

                if ( (LA4_0=='\\') ) {
                    int LA4_2 = input.LA(2);

                    if ( (LA4_2=='\"'||LA4_2=='\''||LA4_2=='\\'||LA4_2=='b'||LA4_2=='f'||LA4_2=='n'||LA4_2=='r'||(LA4_2>='t' && LA4_2<='u')) ) {
                        alt4=1;
                    }
                    else if ( (LA4_2=='*'||LA4_2=='@') ) {
                        alt4=2;
                    }


                }
                else if ( ((LA4_0>='\u0000' && LA4_0<=')')||(LA4_0>='+' && LA4_0<='?')||(LA4_0>='A' && LA4_0<='[')||(LA4_0>=']' && LA4_0<='\uFFFF')) ) {
                    alt4=3;
                }


                switch (alt4) {
            	case 1 :
            	    // InternalDatatypes.g:4445:63: '\\\\' ( 'b' | 't' | 'n' | 'f' | 'r' | 'u' | '\"' | '\\'' | '\\\\' )
            	    {
            	    match('\\'); 
            	    if ( input.LA(1)=='\"'||input.LA(1)=='\''||input.LA(1)=='\\'||input.LA(1)=='b'||input.LA(1)=='f'||input.LA(1)=='n'||input.LA(1)=='r'||(input.LA(1)>='t' && input.LA(1)<='u') ) {
            	        input.consume();

            	    }
            	    else {
            	        MismatchedSetException mse = new MismatchedSetException(null,input);
            	        recover(mse);
            	        throw mse;}


            	    }
            	    break;
            	case 2 :
            	    // InternalDatatypes.g:4445:108: ( '\\\\*' | '\\\\@' )
            	    {
            	    // InternalDatatypes.g:4445:108: ( '\\\\*' | '\\\\@' )
            	    int alt3=2;
            	    int LA3_0 = input.LA(1);

            	    if ( (LA3_0=='\\') ) {
            	        int LA3_1 = input.LA(2);

            	        if ( (LA3_1=='*') ) {
            	            alt3=1;
            	        }
            	        else if ( (LA3_1=='@') ) {
            	            alt3=2;
            	        }
            	        else {
            	            NoViableAltException nvae =
            	                new NoViableAltException("", 3, 1, input);

            	            throw nvae;
            	        }
            	    }
            	    else {
            	        NoViableAltException nvae =
            	            new NoViableAltException("", 3, 0, input);

            	        throw nvae;
            	    }
            	    switch (alt3) {
            	        case 1 :
            	            // InternalDatatypes.g:4445:109: '\\\\*'
            	            {
            	            match("\\*"); 


            	            }
            	            break;
            	        case 2 :
            	            // InternalDatatypes.g:4445:115: '\\\\@'
            	            {
            	            match("\\@"); 


            	            }
            	            break;

            	    }


            	    }
            	    break;
            	case 3 :
            	    // InternalDatatypes.g:4445:122: ~ ( ( '\\\\' | '*' | '@' ) )
            	    {
            	    if ( (input.LA(1)>='\u0000' && input.LA(1)<=')')||(input.LA(1)>='+' && input.LA(1)<='?')||(input.LA(1)>='A' && input.LA(1)<='[')||(input.LA(1)>=']' && input.LA(1)<='\uFFFF') ) {
            	        input.consume();

            	    }
            	    else {
            	        MismatchedSetException mse = new MismatchedSetException(null,input);
            	        recover(mse);
            	        throw mse;}


            	    }
            	    break;

            	default :
            	    break loop4;
                }
            } while (true);


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "RULE_ANNOTATION_STRING"

    // $ANTLR start "RULE_ID"
    public final void mRULE_ID() throws RecognitionException {
        try {
            int _type = RULE_ID;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:4447:9: ( ( '^' )? ( 'a' .. 'z' | 'A' .. 'Z' | '_' ) ( 'a' .. 'z' | 'A' .. 'Z' | '_' | '0' .. '9' )* )
            // InternalDatatypes.g:4447:11: ( '^' )? ( 'a' .. 'z' | 'A' .. 'Z' | '_' ) ( 'a' .. 'z' | 'A' .. 'Z' | '_' | '0' .. '9' )*
            {
            // InternalDatatypes.g:4447:11: ( '^' )?
            int alt5=2;
            int LA5_0 = input.LA(1);

            if ( (LA5_0=='^') ) {
                alt5=1;
            }
            switch (alt5) {
                case 1 :
                    // InternalDatatypes.g:4447:11: '^'
                    {
                    match('^'); 

                    }
                    break;

            }

            if ( (input.LA(1)>='A' && input.LA(1)<='Z')||input.LA(1)=='_'||(input.LA(1)>='a' && input.LA(1)<='z') ) {
                input.consume();

            }
            else {
                MismatchedSetException mse = new MismatchedSetException(null,input);
                recover(mse);
                throw mse;}

            // InternalDatatypes.g:4447:40: ( 'a' .. 'z' | 'A' .. 'Z' | '_' | '0' .. '9' )*
            loop6:
            do {
                int alt6=2;
                int LA6_0 = input.LA(1);

                if ( ((LA6_0>='0' && LA6_0<='9')||(LA6_0>='A' && LA6_0<='Z')||LA6_0=='_'||(LA6_0>='a' && LA6_0<='z')) ) {
                    alt6=1;
                }


                switch (alt6) {
            	case 1 :
            	    // InternalDatatypes.g:
            	    {
            	    if ( (input.LA(1)>='0' && input.LA(1)<='9')||(input.LA(1)>='A' && input.LA(1)<='Z')||input.LA(1)=='_'||(input.LA(1)>='a' && input.LA(1)<='z') ) {
            	        input.consume();

            	    }
            	    else {
            	        MismatchedSetException mse = new MismatchedSetException(null,input);
            	        recover(mse);
            	        throw mse;}


            	    }
            	    break;

            	default :
            	    break loop6;
                }
            } while (true);


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "RULE_ID"

    // $ANTLR start "RULE_INT"
    public final void mRULE_INT() throws RecognitionException {
        try {
            int _type = RULE_INT;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:4449:10: ( ( '0' .. '9' )+ )
            // InternalDatatypes.g:4449:12: ( '0' .. '9' )+
            {
            // InternalDatatypes.g:4449:12: ( '0' .. '9' )+
            int cnt7=0;
            loop7:
            do {
                int alt7=2;
                int LA7_0 = input.LA(1);

                if ( ((LA7_0>='0' && LA7_0<='9')) ) {
                    alt7=1;
                }


                switch (alt7) {
            	case 1 :
            	    // InternalDatatypes.g:4449:13: '0' .. '9'
            	    {
            	    matchRange('0','9'); 

            	    }
            	    break;

            	default :
            	    if ( cnt7 >= 1 ) break loop7;
                        EarlyExitException eee =
                            new EarlyExitException(7, input);
                        throw eee;
                }
                cnt7++;
            } while (true);


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "RULE_INT"

    // $ANTLR start "RULE_STRING"
    public final void mRULE_STRING() throws RecognitionException {
        try {
            int _type = RULE_STRING;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:4451:13: ( ( '\"' ( '\\\\' . | ~ ( ( '\\\\' | '\"' ) ) )* '\"' | '\\'' ( '\\\\' . | ~ ( ( '\\\\' | '\\'' ) ) )* '\\'' ) )
            // InternalDatatypes.g:4451:15: ( '\"' ( '\\\\' . | ~ ( ( '\\\\' | '\"' ) ) )* '\"' | '\\'' ( '\\\\' . | ~ ( ( '\\\\' | '\\'' ) ) )* '\\'' )
            {
            // InternalDatatypes.g:4451:15: ( '\"' ( '\\\\' . | ~ ( ( '\\\\' | '\"' ) ) )* '\"' | '\\'' ( '\\\\' . | ~ ( ( '\\\\' | '\\'' ) ) )* '\\'' )
            int alt10=2;
            int LA10_0 = input.LA(1);

            if ( (LA10_0=='\"') ) {
                alt10=1;
            }
            else if ( (LA10_0=='\'') ) {
                alt10=2;
            }
            else {
                NoViableAltException nvae =
                    new NoViableAltException("", 10, 0, input);

                throw nvae;
            }
            switch (alt10) {
                case 1 :
                    // InternalDatatypes.g:4451:16: '\"' ( '\\\\' . | ~ ( ( '\\\\' | '\"' ) ) )* '\"'
                    {
                    match('\"'); 
                    // InternalDatatypes.g:4451:20: ( '\\\\' . | ~ ( ( '\\\\' | '\"' ) ) )*
                    loop8:
                    do {
                        int alt8=3;
                        int LA8_0 = input.LA(1);

                        if ( (LA8_0=='\\') ) {
                            alt8=1;
                        }
                        else if ( ((LA8_0>='\u0000' && LA8_0<='!')||(LA8_0>='#' && LA8_0<='[')||(LA8_0>=']' && LA8_0<='\uFFFF')) ) {
                            alt8=2;
                        }


                        switch (alt8) {
                    	case 1 :
                    	    // InternalDatatypes.g:4451:21: '\\\\' .
                    	    {
                    	    match('\\'); 
                    	    matchAny(); 

                    	    }
                    	    break;
                    	case 2 :
                    	    // InternalDatatypes.g:4451:28: ~ ( ( '\\\\' | '\"' ) )
                    	    {
                    	    if ( (input.LA(1)>='\u0000' && input.LA(1)<='!')||(input.LA(1)>='#' && input.LA(1)<='[')||(input.LA(1)>=']' && input.LA(1)<='\uFFFF') ) {
                    	        input.consume();

                    	    }
                    	    else {
                    	        MismatchedSetException mse = new MismatchedSetException(null,input);
                    	        recover(mse);
                    	        throw mse;}


                    	    }
                    	    break;

                    	default :
                    	    break loop8;
                        }
                    } while (true);

                    match('\"'); 

                    }
                    break;
                case 2 :
                    // InternalDatatypes.g:4451:48: '\\'' ( '\\\\' . | ~ ( ( '\\\\' | '\\'' ) ) )* '\\''
                    {
                    match('\''); 
                    // InternalDatatypes.g:4451:53: ( '\\\\' . | ~ ( ( '\\\\' | '\\'' ) ) )*
                    loop9:
                    do {
                        int alt9=3;
                        int LA9_0 = input.LA(1);

                        if ( (LA9_0=='\\') ) {
                            alt9=1;
                        }
                        else if ( ((LA9_0>='\u0000' && LA9_0<='&')||(LA9_0>='(' && LA9_0<='[')||(LA9_0>=']' && LA9_0<='\uFFFF')) ) {
                            alt9=2;
                        }


                        switch (alt9) {
                    	case 1 :
                    	    // InternalDatatypes.g:4451:54: '\\\\' .
                    	    {
                    	    match('\\'); 
                    	    matchAny(); 

                    	    }
                    	    break;
                    	case 2 :
                    	    // InternalDatatypes.g:4451:61: ~ ( ( '\\\\' | '\\'' ) )
                    	    {
                    	    if ( (input.LA(1)>='\u0000' && input.LA(1)<='&')||(input.LA(1)>='(' && input.LA(1)<='[')||(input.LA(1)>=']' && input.LA(1)<='\uFFFF') ) {
                    	        input.consume();

                    	    }
                    	    else {
                    	        MismatchedSetException mse = new MismatchedSetException(null,input);
                    	        recover(mse);
                    	        throw mse;}


                    	    }
                    	    break;

                    	default :
                    	    break loop9;
                        }
                    } while (true);

                    match('\''); 

                    }
                    break;

            }


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "RULE_STRING"

    // $ANTLR start "RULE_ML_COMMENT"
    public final void mRULE_ML_COMMENT() throws RecognitionException {
        try {
            int _type = RULE_ML_COMMENT;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:4453:17: ( '/*' ( options {greedy=false; } : . )* '*/' )
            // InternalDatatypes.g:4453:19: '/*' ( options {greedy=false; } : . )* '*/'
            {
            match("/*"); 

            // InternalDatatypes.g:4453:24: ( options {greedy=false; } : . )*
            loop11:
            do {
                int alt11=2;
                int LA11_0 = input.LA(1);

                if ( (LA11_0=='*') ) {
                    int LA11_1 = input.LA(2);

                    if ( (LA11_1=='/') ) {
                        alt11=2;
                    }
                    else if ( ((LA11_1>='\u0000' && LA11_1<='.')||(LA11_1>='0' && LA11_1<='\uFFFF')) ) {
                        alt11=1;
                    }


                }
                else if ( ((LA11_0>='\u0000' && LA11_0<=')')||(LA11_0>='+' && LA11_0<='\uFFFF')) ) {
                    alt11=1;
                }


                switch (alt11) {
            	case 1 :
            	    // InternalDatatypes.g:4453:52: .
            	    {
            	    matchAny(); 

            	    }
            	    break;

            	default :
            	    break loop11;
                }
            } while (true);

            match("*/"); 


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "RULE_ML_COMMENT"

    // $ANTLR start "RULE_SL_COMMENT"
    public final void mRULE_SL_COMMENT() throws RecognitionException {
        try {
            int _type = RULE_SL_COMMENT;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:4455:17: ( '//' (~ ( ( '\\n' | '\\r' ) ) )* ( ( '\\r' )? '\\n' )? )
            // InternalDatatypes.g:4455:19: '//' (~ ( ( '\\n' | '\\r' ) ) )* ( ( '\\r' )? '\\n' )?
            {
            match("//"); 

            // InternalDatatypes.g:4455:24: (~ ( ( '\\n' | '\\r' ) ) )*
            loop12:
            do {
                int alt12=2;
                int LA12_0 = input.LA(1);

                if ( ((LA12_0>='\u0000' && LA12_0<='\t')||(LA12_0>='\u000B' && LA12_0<='\f')||(LA12_0>='\u000E' && LA12_0<='\uFFFF')) ) {
                    alt12=1;
                }


                switch (alt12) {
            	case 1 :
            	    // InternalDatatypes.g:4455:24: ~ ( ( '\\n' | '\\r' ) )
            	    {
            	    if ( (input.LA(1)>='\u0000' && input.LA(1)<='\t')||(input.LA(1)>='\u000B' && input.LA(1)<='\f')||(input.LA(1)>='\u000E' && input.LA(1)<='\uFFFF') ) {
            	        input.consume();

            	    }
            	    else {
            	        MismatchedSetException mse = new MismatchedSetException(null,input);
            	        recover(mse);
            	        throw mse;}


            	    }
            	    break;

            	default :
            	    break loop12;
                }
            } while (true);

            // InternalDatatypes.g:4455:40: ( ( '\\r' )? '\\n' )?
            int alt14=2;
            int LA14_0 = input.LA(1);

            if ( (LA14_0=='\n'||LA14_0=='\r') ) {
                alt14=1;
            }
            switch (alt14) {
                case 1 :
                    // InternalDatatypes.g:4455:41: ( '\\r' )? '\\n'
                    {
                    // InternalDatatypes.g:4455:41: ( '\\r' )?
                    int alt13=2;
                    int LA13_0 = input.LA(1);

                    if ( (LA13_0=='\r') ) {
                        alt13=1;
                    }
                    switch (alt13) {
                        case 1 :
                            // InternalDatatypes.g:4455:41: '\\r'
                            {
                            match('\r'); 

                            }
                            break;

                    }

                    match('\n'); 

                    }
                    break;

            }


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "RULE_SL_COMMENT"

    // $ANTLR start "RULE_WS"
    public final void mRULE_WS() throws RecognitionException {
        try {
            int _type = RULE_WS;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:4457:9: ( ( ' ' | '\\t' | '\\r' | '\\n' )+ )
            // InternalDatatypes.g:4457:11: ( ' ' | '\\t' | '\\r' | '\\n' )+
            {
            // InternalDatatypes.g:4457:11: ( ' ' | '\\t' | '\\r' | '\\n' )+
            int cnt15=0;
            loop15:
            do {
                int alt15=2;
                int LA15_0 = input.LA(1);

                if ( ((LA15_0>='\t' && LA15_0<='\n')||LA15_0=='\r'||LA15_0==' ') ) {
                    alt15=1;
                }


                switch (alt15) {
            	case 1 :
            	    // InternalDatatypes.g:
            	    {
            	    if ( (input.LA(1)>='\t' && input.LA(1)<='\n')||input.LA(1)=='\r'||input.LA(1)==' ' ) {
            	        input.consume();

            	    }
            	    else {
            	        MismatchedSetException mse = new MismatchedSetException(null,input);
            	        recover(mse);
            	        throw mse;}


            	    }
            	    break;

            	default :
            	    if ( cnt15 >= 1 ) break loop15;
                        EarlyExitException eee =
                            new EarlyExitException(15, input);
                        throw eee;
                }
                cnt15++;
            } while (true);


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "RULE_WS"

    // $ANTLR start "RULE_ANY_OTHER"
    public final void mRULE_ANY_OTHER() throws RecognitionException {
        try {
            int _type = RULE_ANY_OTHER;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // InternalDatatypes.g:4459:16: ( . )
            // InternalDatatypes.g:4459:18: .
            {
            matchAny(); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        }
    }
    // $ANTLR end "RULE_ANY_OTHER"

    public void mTokens() throws RecognitionException {
        // InternalDatatypes.g:1:8: ( T__12 | T__13 | T__14 | T__15 | T__16 | T__17 | T__18 | T__19 | T__20 | T__21 | T__22 | T__23 | T__24 | T__25 | T__26 | T__27 | T__28 | T__29 | T__30 | T__31 | T__32 | T__33 | T__34 | T__35 | T__36 | T__37 | T__38 | T__39 | T__40 | T__41 | T__42 | T__43 | T__44 | T__45 | T__46 | T__47 | T__48 | T__49 | T__50 | T__51 | RULE_ANNOTATION_STRING | RULE_ID | RULE_INT | RULE_STRING | RULE_ML_COMMENT | RULE_SL_COMMENT | RULE_WS | RULE_ANY_OTHER )
        int alt16=48;
        alt16 = dfa16.predict(input);
        switch (alt16) {
            case 1 :
                // InternalDatatypes.g:1:10: T__12
                {
                mT__12(); 

                }
                break;
            case 2 :
                // InternalDatatypes.g:1:16: T__13
                {
                mT__13(); 

                }
                break;
            case 3 :
                // InternalDatatypes.g:1:22: T__14
                {
                mT__14(); 

                }
                break;
            case 4 :
                // InternalDatatypes.g:1:28: T__15
                {
                mT__15(); 

                }
                break;
            case 5 :
                // InternalDatatypes.g:1:34: T__16
                {
                mT__16(); 

                }
                break;
            case 6 :
                // InternalDatatypes.g:1:40: T__17
                {
                mT__17(); 

                }
                break;
            case 7 :
                // InternalDatatypes.g:1:46: T__18
                {
                mT__18(); 

                }
                break;
            case 8 :
                // InternalDatatypes.g:1:52: T__19
                {
                mT__19(); 

                }
                break;
            case 9 :
                // InternalDatatypes.g:1:58: T__20
                {
                mT__20(); 

                }
                break;
            case 10 :
                // InternalDatatypes.g:1:64: T__21
                {
                mT__21(); 

                }
                break;
            case 11 :
                // InternalDatatypes.g:1:70: T__22
                {
                mT__22(); 

                }
                break;
            case 12 :
                // InternalDatatypes.g:1:76: T__23
                {
                mT__23(); 

                }
                break;
            case 13 :
                // InternalDatatypes.g:1:82: T__24
                {
                mT__24(); 

                }
                break;
            case 14 :
                // InternalDatatypes.g:1:88: T__25
                {
                mT__25(); 

                }
                break;
            case 15 :
                // InternalDatatypes.g:1:94: T__26
                {
                mT__26(); 

                }
                break;
            case 16 :
                // InternalDatatypes.g:1:100: T__27
                {
                mT__27(); 

                }
                break;
            case 17 :
                // InternalDatatypes.g:1:106: T__28
                {
                mT__28(); 

                }
                break;
            case 18 :
                // InternalDatatypes.g:1:112: T__29
                {
                mT__29(); 

                }
                break;
            case 19 :
                // InternalDatatypes.g:1:118: T__30
                {
                mT__30(); 

                }
                break;
            case 20 :
                // InternalDatatypes.g:1:124: T__31
                {
                mT__31(); 

                }
                break;
            case 21 :
                // InternalDatatypes.g:1:130: T__32
                {
                mT__32(); 

                }
                break;
            case 22 :
                // InternalDatatypes.g:1:136: T__33
                {
                mT__33(); 

                }
                break;
            case 23 :
                // InternalDatatypes.g:1:142: T__34
                {
                mT__34(); 

                }
                break;
            case 24 :
                // InternalDatatypes.g:1:148: T__35
                {
                mT__35(); 

                }
                break;
            case 25 :
                // InternalDatatypes.g:1:154: T__36
                {
                mT__36(); 

                }
                break;
            case 26 :
                // InternalDatatypes.g:1:160: T__37
                {
                mT__37(); 

                }
                break;
            case 27 :
                // InternalDatatypes.g:1:166: T__38
                {
                mT__38(); 

                }
                break;
            case 28 :
                // InternalDatatypes.g:1:172: T__39
                {
                mT__39(); 

                }
                break;
            case 29 :
                // InternalDatatypes.g:1:178: T__40
                {
                mT__40(); 

                }
                break;
            case 30 :
                // InternalDatatypes.g:1:184: T__41
                {
                mT__41(); 

                }
                break;
            case 31 :
                // InternalDatatypes.g:1:190: T__42
                {
                mT__42(); 

                }
                break;
            case 32 :
                // InternalDatatypes.g:1:196: T__43
                {
                mT__43(); 

                }
                break;
            case 33 :
                // InternalDatatypes.g:1:202: T__44
                {
                mT__44(); 

                }
                break;
            case 34 :
                // InternalDatatypes.g:1:208: T__45
                {
                mT__45(); 

                }
                break;
            case 35 :
                // InternalDatatypes.g:1:214: T__46
                {
                mT__46(); 

                }
                break;
            case 36 :
                // InternalDatatypes.g:1:220: T__47
                {
                mT__47(); 

                }
                break;
            case 37 :
                // InternalDatatypes.g:1:226: T__48
                {
                mT__48(); 

                }
                break;
            case 38 :
                // InternalDatatypes.g:1:232: T__49
                {
                mT__49(); 

                }
                break;
            case 39 :
                // InternalDatatypes.g:1:238: T__50
                {
                mT__50(); 

                }
                break;
            case 40 :
                // InternalDatatypes.g:1:244: T__51
                {
                mT__51(); 

                }
                break;
            case 41 :
                // InternalDatatypes.g:1:250: RULE_ANNOTATION_STRING
                {
                mRULE_ANNOTATION_STRING(); 

                }
                break;
            case 42 :
                // InternalDatatypes.g:1:273: RULE_ID
                {
                mRULE_ID(); 

                }
                break;
            case 43 :
                // InternalDatatypes.g:1:281: RULE_INT
                {
                mRULE_INT(); 

                }
                break;
            case 44 :
                // InternalDatatypes.g:1:290: RULE_STRING
                {
                mRULE_STRING(); 

                }
                break;
            case 45 :
                // InternalDatatypes.g:1:302: RULE_ML_COMMENT
                {
                mRULE_ML_COMMENT(); 

                }
                break;
            case 46 :
                // InternalDatatypes.g:1:318: RULE_SL_COMMENT
                {
                mRULE_SL_COMMENT(); 

                }
                break;
            case 47 :
                // InternalDatatypes.g:1:334: RULE_WS
                {
                mRULE_WS(); 

                }
                break;
            case 48 :
                // InternalDatatypes.g:1:342: RULE_ANY_OTHER
                {
                mRULE_ANY_OTHER(); 

                }
                break;

        }

    }


    protected DFA16 dfa16 = new DFA16(this);
    static final String DFA16_eotS =
        "\1\uffff\10\44\1\uffff\1\60\1\42\1\44\2\uffff\7\44\4\uffff\2\42\2\uffff\3\42\2\uffff\1\44\1\uffff\10\44\1\123\4\uffff\1\44\1\125\2\uffff\6\44\1\135\3\44\12\uffff\11\44\1\uffff\1\44\1\uffff\3\44\1\161\1\44\1\163\1\44\1\uffff\3\44\1\170\17\44\1\uffff\1\44\1\uffff\4\44\1\uffff\1\u0091\1\u0092\1\u0093\1\u0094\6\44\1\u009b\7\44\1\u00a3\1\u00a4\1\u00a5\3\44\4\uffff\1\u00a9\1\u00aa\1\u00ab\2\44\1\u00ae\1\uffff\1\u00af\1\44\1\u00b1\4\44\3\uffff\1\u00b6\2\44\3\uffff\1\u00b9\1\44\2\uffff\1\u00bb\1\uffff\1\44\1\u00bd\1\u00be\1\44\1\uffff\1\u00c0\1\44\1\uffff\1\44\1\uffff\1\44\2\uffff\1\44\1\uffff\5\44\1\u00ca\3\44\1\uffff\2\44\1\u00d0\2\44\1\uffff\2\44\1\u00d5\1\44\1\uffff\2\44\1\u00d9\1\uffff";
    static final String DFA16_eofS =
        "\u00da\uffff";
    static final String DFA16_minS =
        "\1\0\1\156\1\111\1\157\1\164\1\154\1\157\1\141\1\155\1\uffff\2\52\1\157\2\uffff\1\145\1\141\1\145\1\162\1\146\1\164\1\156\4\uffff\1\55\1\101\2\uffff\2\0\1\52\2\uffff\1\164\1\uffff\1\156\1\157\1\164\1\162\1\157\1\165\1\143\1\160\1\60\4\uffff\1\160\1\60\2\uffff\1\162\1\163\1\152\1\156\1\171\1\162\1\60\1\162\1\164\1\165\12\uffff\1\61\1\164\1\154\1\145\1\151\1\141\1\142\1\153\1\157\1\uffff\1\145\1\uffff\2\163\1\157\1\60\1\157\1\60\1\141\1\uffff\1\165\1\145\1\155\1\60\1\66\1\62\1\64\1\61\1\145\1\102\1\156\1\164\1\154\1\141\1\162\1\103\1\151\1\141\1\162\1\uffff\1\162\1\uffff\1\171\1\143\1\156\1\145\1\uffff\4\60\1\66\1\62\1\64\1\141\1\165\1\147\1\60\1\145\1\147\1\164\1\157\1\145\1\157\1\147\3\60\1\164\1\144\1\162\4\uffff\3\60\1\156\1\146\1\60\1\uffff\1\60\1\145\1\60\1\154\1\146\1\156\1\145\3\uffff\1\60\1\163\1\141\3\uffff\1\60\1\146\2\uffff\1\60\1\uffff\1\154\2\60\1\103\1\uffff\1\60\1\164\1\uffff\1\145\1\uffff\1\145\2\uffff\1\157\1\uffff\1\151\1\162\1\143\1\154\1\157\1\60\1\164\1\154\1\156\1\uffff\1\151\1\145\1\60\1\157\1\143\1\uffff\1\156\1\164\1\60\1\151\1\uffff\1\157\1\156\1\60\1\uffff";
    static final String DFA16_maxS =
        "\1\uffff\1\156\1\111\1\171\1\164\1\154\1\157\1\141\1\163\1\uffff\2\52\1\171\2\uffff\1\145\1\151\1\145\1\162\1\146\1\164\1\170\4\uffff\2\172\2\uffff\2\uffff\1\57\2\uffff\1\164\1\uffff\1\156\1\157\1\164\1\162\1\157\1\165\1\143\1\160\1\172\4\uffff\1\160\1\172\2\uffff\1\162\1\163\1\160\1\156\1\171\1\162\1\172\1\162\1\164\1\165\12\uffff\1\70\1\164\1\154\1\145\1\151\1\141\1\142\1\153\1\157\1\uffff\1\145\1\uffff\2\163\1\157\1\172\1\157\1\172\1\141\1\uffff\1\165\1\145\1\155\1\172\1\66\1\62\1\64\1\70\1\145\1\102\1\156\1\164\1\154\1\141\1\162\1\144\1\151\1\141\1\162\1\uffff\1\162\1\uffff\1\171\1\143\1\156\1\145\1\uffff\4\172\1\66\1\62\1\64\1\141\1\165\1\147\1\172\1\145\1\147\1\164\1\157\1\145\1\157\1\147\3\172\1\164\1\144\1\162\4\uffff\3\172\1\156\1\146\1\172\1\uffff\1\172\1\145\1\172\1\154\1\146\1\156\1\145\3\uffff\1\172\1\163\1\141\3\uffff\1\172\1\146\2\uffff\1\172\1\uffff\1\154\2\172\1\103\1\uffff\1\172\1\164\1\uffff\1\145\1\uffff\1\145\2\uffff\1\157\1\uffff\1\151\1\162\1\143\1\154\1\157\1\172\1\164\1\154\1\156\1\uffff\1\151\1\145\1\172\1\157\1\143\1\uffff\1\156\1\164\1\172\1\151\1\uffff\1\157\1\156\1\172\1\uffff";
    static final String DFA16_acceptS =
        "\11\uffff\1\20\3\uffff\1\25\1\26\7\uffff\1\43\1\44\1\47\1\50\2\uffff\1\52\1\53\3\uffff\1\57\1\60\1\uffff\1\52\11\uffff\1\20\1\23\1\21\1\22\2\uffff\1\25\1\26\12\uffff\1\43\1\44\1\47\1\50\1\51\1\53\1\54\1\55\1\56\1\57\11\uffff\1\37\1\uffff\1\46\7\uffff\1\35\23\uffff\1\45\1\uffff\1\31\4\uffff\1\1\30\uffff\1\3\1\5\1\7\1\2\6\uffff\1\13\7\uffff\1\32\1\33\1\34\3\uffff\1\4\1\6\1\10\2\uffff\1\12\1\14\1\uffff\1\17\4\uffff\1\40\2\uffff\1\11\1\uffff\1\16\1\uffff\1\36\1\27\1\uffff\1\41\11\uffff\1\15\5\uffff\1\42\4\uffff\1\24\3\uffff\1\30";
    static final String DFA16_specialS =
        "\1\2\35\uffff\1\0\1\1\u00ba\uffff}>";
    static final String[] DFA16_transitionS = {
            "\11\42\2\41\2\42\1\41\22\42\1\41\1\42\1\36\4\42\1\37\2\42\1\12\1\42\1\26\1\42\1\11\1\40\12\35\2\42\1\13\1\27\2\42\1\32\1\34\1\3\1\34\1\6\1\34\1\5\2\34\1\1\11\34\1\4\1\34\1\2\5\34\1\31\1\42\1\30\1\33\1\34\1\42\1\22\3\34\1\25\3\34\1\10\1\34\1\21\1\34\1\20\1\34\1\23\1\7\2\34\1\24\1\14\1\34\1\17\4\34\1\15\1\42\1\16\uff82\42",
            "\1\43",
            "\1\45",
            "\1\46\11\uffff\1\47",
            "\1\50",
            "\1\51",
            "\1\52",
            "\1\53",
            "\1\54\5\uffff\1\55",
            "",
            "\1\57",
            "\1\61",
            "\1\63\11\uffff\1\62",
            "",
            "",
            "\1\66",
            "\1\70\3\uffff\1\67\3\uffff\1\71",
            "\1\72",
            "\1\73",
            "\1\74",
            "\1\75",
            "\1\77\11\uffff\1\76",
            "",
            "",
            "",
            "",
            "\1\104\63\uffff\32\104",
            "\32\44\4\uffff\1\44\1\uffff\32\44",
            "",
            "",
            "\0\106",
            "\0\106",
            "\1\107\4\uffff\1\110",
            "",
            "",
            "\1\112",
            "",
            "\1\113",
            "\1\114",
            "\1\115",
            "\1\116",
            "\1\117",
            "\1\120",
            "\1\121",
            "\1\122",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "",
            "",
            "",
            "",
            "\1\124",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "",
            "",
            "\1\126",
            "\1\127",
            "\1\130\5\uffff\1\131",
            "\1\132",
            "\1\133",
            "\1\134",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\1\136",
            "\1\137",
            "\1\140",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "\1\142\1\uffff\1\143\2\uffff\1\144\1\uffff\1\141",
            "\1\145",
            "\1\146",
            "\1\147",
            "\1\150",
            "\1\151",
            "\1\152",
            "\1\153",
            "\1\154",
            "",
            "\1\155",
            "",
            "\1\156",
            "\1\157",
            "\1\160",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\1\162",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\1\164",
            "",
            "\1\165",
            "\1\166",
            "\1\167",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\1\171",
            "\1\172",
            "\1\173",
            "\1\175\1\uffff\1\176\2\uffff\1\177\1\uffff\1\174",
            "\1\u0080",
            "\1\u0081",
            "\1\u0082",
            "\1\u0083",
            "\1\u0084",
            "\1\u0085",
            "\1\u0086",
            "\1\u0087\40\uffff\1\u0088",
            "\1\u0089",
            "\1\u008a",
            "\1\u008b",
            "",
            "\1\u008c",
            "",
            "\1\u008d",
            "\1\u008e",
            "\1\u008f",
            "\1\u0090",
            "",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\1\u0095",
            "\1\u0096",
            "\1\u0097",
            "\1\u0098",
            "\1\u0099",
            "\1\u009a",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\1\u009c",
            "\1\u009d",
            "\1\u009e",
            "\1\u009f",
            "\1\u00a0",
            "\1\u00a1",
            "\1\u00a2",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\1\u00a6",
            "\1\u00a7",
            "\1\u00a8",
            "",
            "",
            "",
            "",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\1\u00ac",
            "\1\u00ad",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\1\u00b0",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\1\u00b2",
            "\1\u00b3",
            "\1\u00b4",
            "\1\u00b5",
            "",
            "",
            "",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\1\u00b7",
            "\1\u00b8",
            "",
            "",
            "",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\1\u00ba",
            "",
            "",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "",
            "\1\u00bc",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\1\u00bf",
            "",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\1\u00c1",
            "",
            "\1\u00c2",
            "",
            "\1\u00c3",
            "",
            "",
            "\1\u00c4",
            "",
            "\1\u00c5",
            "\1\u00c6",
            "\1\u00c7",
            "\1\u00c8",
            "\1\u00c9",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\1\u00cb",
            "\1\u00cc",
            "\1\u00cd",
            "",
            "\1\u00ce",
            "\1\u00cf",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\1\u00d1",
            "\1\u00d2",
            "",
            "\1\u00d3",
            "\1\u00d4",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            "\1\u00d6",
            "",
            "\1\u00d7",
            "\1\u00d8",
            "\12\44\7\uffff\32\44\4\uffff\1\44\1\uffff\32\44",
            ""
    };

    static final short[] DFA16_eot = DFA.unpackEncodedString(DFA16_eotS);
    static final short[] DFA16_eof = DFA.unpackEncodedString(DFA16_eofS);
    static final char[] DFA16_min = DFA.unpackEncodedStringToUnsignedChars(DFA16_minS);
    static final char[] DFA16_max = DFA.unpackEncodedStringToUnsignedChars(DFA16_maxS);
    static final short[] DFA16_accept = DFA.unpackEncodedString(DFA16_acceptS);
    static final short[] DFA16_special = DFA.unpackEncodedString(DFA16_specialS);
    static final short[][] DFA16_transition;

    static {
        int numStates = DFA16_transitionS.length;
        DFA16_transition = new short[numStates][];
        for (int i=0; i<numStates; i++) {
            DFA16_transition[i] = DFA.unpackEncodedString(DFA16_transitionS[i]);
        }
    }

    class DFA16 extends DFA {

        public DFA16(BaseRecognizer recognizer) {
            this.recognizer = recognizer;
            this.decisionNumber = 16;
            this.eot = DFA16_eot;
            this.eof = DFA16_eof;
            this.min = DFA16_min;
            this.max = DFA16_max;
            this.accept = DFA16_accept;
            this.special = DFA16_special;
            this.transition = DFA16_transition;
        }
        public String getDescription() {
            return "1:1: Tokens : ( T__12 | T__13 | T__14 | T__15 | T__16 | T__17 | T__18 | T__19 | T__20 | T__21 | T__22 | T__23 | T__24 | T__25 | T__26 | T__27 | T__28 | T__29 | T__30 | T__31 | T__32 | T__33 | T__34 | T__35 | T__36 | T__37 | T__38 | T__39 | T__40 | T__41 | T__42 | T__43 | T__44 | T__45 | T__46 | T__47 | T__48 | T__49 | T__50 | T__51 | RULE_ANNOTATION_STRING | RULE_ID | RULE_INT | RULE_STRING | RULE_ML_COMMENT | RULE_SL_COMMENT | RULE_WS | RULE_ANY_OTHER );";
        }
        public int specialStateTransition(int s, IntStream _input) throws NoViableAltException {
            IntStream input = _input;
        	int _s = s;
            switch ( s ) {
                    case 0 : 
                        int LA16_30 = input.LA(1);

                        s = -1;
                        if ( ((LA16_30>='\u0000' && LA16_30<='\uFFFF')) ) {s = 70;}

                        else s = 34;

                        if ( s>=0 ) return s;
                        break;
                    case 1 : 
                        int LA16_31 = input.LA(1);

                        s = -1;
                        if ( ((LA16_31>='\u0000' && LA16_31<='\uFFFF')) ) {s = 70;}

                        else s = 34;

                        if ( s>=0 ) return s;
                        break;
                    case 2 : 
                        int LA16_0 = input.LA(1);

                        s = -1;
                        if ( (LA16_0=='I') ) {s = 1;}

                        else if ( (LA16_0=='U') ) {s = 2;}

                        else if ( (LA16_0=='B') ) {s = 3;}

                        else if ( (LA16_0=='S') ) {s = 4;}

                        else if ( (LA16_0=='F') ) {s = 5;}

                        else if ( (LA16_0=='D') ) {s = 6;}

                        else if ( (LA16_0=='p') ) {s = 7;}

                        else if ( (LA16_0=='i') ) {s = 8;}

                        else if ( (LA16_0=='.') ) {s = 9;}

                        else if ( (LA16_0=='*') ) {s = 10;}

                        else if ( (LA16_0=='<') ) {s = 11;}

                        else if ( (LA16_0=='t') ) {s = 12;}

                        else if ( (LA16_0=='{') ) {s = 13;}

                        else if ( (LA16_0=='}') ) {s = 14;}

                        else if ( (LA16_0=='v') ) {s = 15;}

                        else if ( (LA16_0=='m') ) {s = 16;}

                        else if ( (LA16_0=='k') ) {s = 17;}

                        else if ( (LA16_0=='a') ) {s = 18;}

                        else if ( (LA16_0=='o') ) {s = 19;}

                        else if ( (LA16_0=='s') ) {s = 20;}

                        else if ( (LA16_0=='e') ) {s = 21;}

                        else if ( (LA16_0==',') ) {s = 22;}

                        else if ( (LA16_0=='=') ) {s = 23;}

                        else if ( (LA16_0==']') ) {s = 24;}

                        else if ( (LA16_0=='[') ) {s = 25;}

                        else if ( (LA16_0=='@') ) {s = 26;}

                        else if ( (LA16_0=='^') ) {s = 27;}

                        else if ( (LA16_0=='A'||LA16_0=='C'||LA16_0=='E'||(LA16_0>='G' && LA16_0<='H')||(LA16_0>='J' && LA16_0<='R')||LA16_0=='T'||(LA16_0>='V' && LA16_0<='Z')||LA16_0=='_'||(LA16_0>='b' && LA16_0<='d')||(LA16_0>='f' && LA16_0<='h')||LA16_0=='j'||LA16_0=='l'||LA16_0=='n'||(LA16_0>='q' && LA16_0<='r')||LA16_0=='u'||(LA16_0>='w' && LA16_0<='z')) ) {s = 28;}

                        else if ( ((LA16_0>='0' && LA16_0<='9')) ) {s = 29;}

                        else if ( (LA16_0=='\"') ) {s = 30;}

                        else if ( (LA16_0=='\'') ) {s = 31;}

                        else if ( (LA16_0=='/') ) {s = 32;}

                        else if ( ((LA16_0>='\t' && LA16_0<='\n')||LA16_0=='\r'||LA16_0==' ') ) {s = 33;}

                        else if ( ((LA16_0>='\u0000' && LA16_0<='\b')||(LA16_0>='\u000B' && LA16_0<='\f')||(LA16_0>='\u000E' && LA16_0<='\u001F')||LA16_0=='!'||(LA16_0>='#' && LA16_0<='&')||(LA16_0>='(' && LA16_0<=')')||LA16_0=='+'||LA16_0=='-'||(LA16_0>=':' && LA16_0<=';')||(LA16_0>='>' && LA16_0<='?')||LA16_0=='\\'||LA16_0=='`'||LA16_0=='|'||(LA16_0>='~' && LA16_0<='\uFFFF')) ) {s = 34;}

                        if ( s>=0 ) return s;
                        break;
            }
            NoViableAltException nvae =
                new NoViableAltException(getDescription(), 16, _s, input);
            error(nvae);
            throw nvae;
        }
    }
 

}